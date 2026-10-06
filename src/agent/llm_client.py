"""Member 2 - LLM client interface. One method: complete(system, user) -> str.
Real provider clients (Gemini/OpenAI/Anthropic) are added once the team picks one.
"""
from typing import List, Protocol


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