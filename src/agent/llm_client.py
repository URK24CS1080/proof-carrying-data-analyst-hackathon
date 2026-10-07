"""Member 2 - LLM client. One method: complete(system, user) -> str.

GeminiClient is the real client. MockLLM is for tests. To switch provider later,
write another class with the same complete() method and change get_llm().

Transient errors (429 rate limit, 500/502/503/504 overload) are retried with a
short backoff, then an optional fallback model is tried. Other errors (bad key,
unknown model) are raised immediately.
"""
import os
import time
from typing import List, Optional, Protocol

DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"  # override with GEMINI_MODEL in .env
RETRY_CODES = {429, 500, 502, 503, 504}


class LLMClient(Protocol):
    def complete(self, system: str, user: str) -> str: ...


class MockLLM:
    """Test double: returns canned responses in order (repeats the last one)."""

    def __init__(self, responses: List[str]):
        self.responses = list(responses)
        self.calls: List[tuple] = []

    def complete(self, system: str, user: str) -> str:
        self.calls.append((system, user))
        i = min(len(self.calls) - 1, len(self.responses) - 1)
        return self.responses[i]


def _is_transient(e: Exception) -> bool:
    if getattr(e, "code", None) in RETRY_CODES:
        return True
    msg = str(e)
    return any(t in msg for t in ("503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED"))


class GeminiClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None,
                 fallback_model: Optional[str] = None, max_retries: int = 3):
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Put it in a .env file in the project root: "
                "GEMINI_API_KEY=your_key_here"
            )
        from google import genai
        from google.genai import types

        self._types = types
        self._client = genai.Client(api_key=key)
        self.model = model or os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
        self.fallback_model = fallback_model or os.getenv("GEMINI_FALLBACK_MODEL")
        self.max_retries = max_retries
        self._sleep = time.sleep  # replaceable in tests

    def _generate(self, model: str, system: str, user: str) -> str:
        resp = self._client.models.generate_content(
            model=model,
            contents=user,
            config=self._types.GenerateContentConfig(
                system_instruction=system,
                response_mime_type="application/json",
                temperature=0,
            ),
        )
        return resp.text or ""

    def complete(self, system: str, user: str) -> str:
        models = [self.model]
        if self.fallback_model and self.fallback_model != self.model:
            models.append(self.fallback_model)
        last: Optional[Exception] = None
        for m in models:
            for attempt in range(self.max_retries + 1):
                try:
                    return self._generate(m, system, user)
                except Exception as e:
                    last = e
                    if not _is_transient(e):
                        raise
                    if attempt < self.max_retries:
                        self._sleep(2 ** attempt)  # waits 1s, 2s, 4s
        assert last is not None
        raise last


def get_llm() -> LLMClient:
    """The single place the rest of the project asks for an LLM."""
    return GeminiClient()