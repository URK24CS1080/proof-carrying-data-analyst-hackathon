import sys
import types

import pytest

from src.agent import llm_client


def _install_fake_genai(monkeypatch, reply_text):
    seen = {}

    class _Models:
        def generate_content(self, model, contents, config):
            seen.update(model=model, contents=contents, config=config)
            return types.SimpleNamespace(text=reply_text)

    class _Client:
        def __init__(self, api_key):
            seen["api_key"] = api_key
            self.models = _Models()

    class _Config:
        def __init__(self, **kw):
            self.__dict__.update(kw)

    genai = types.ModuleType("google.genai")
    genai.Client = _Client
    genai.types = types.SimpleNamespace(GenerateContentConfig=_Config)
    google = types.ModuleType("google")
    google.genai = genai
    monkeypatch.setitem(sys.modules, "google", google)
    monkeypatch.setitem(sys.modules, "google.genai", genai)
    monkeypatch.setitem(sys.modules, "google.genai.types", genai.types)
    return seen


def test_gemini_client_sends_json_mode_and_returns_text(monkeypatch):
    seen = _install_fake_genai(monkeypatch, '{"status":"cannot_determine","reason":"x"}')
    c = llm_client.GeminiClient(api_key="k", model="m1")
    out = c.complete("SYS", "USER")
    assert out.startswith("{")
    assert seen["model"] == "m1" and seen["contents"] == "USER" and seen["api_key"] == "k"
    assert seen["config"].system_instruction == "SYS"
    assert seen["config"].response_mime_type == "application/json"
    assert seen["config"].temperature == 0


def test_missing_key_gives_clear_error(monkeypatch):
    _install_fake_genai(monkeypatch, "{}")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setitem(sys.modules, "dotenv", None)  # block .env loading so the test is hermetic
    with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
        llm_client.GeminiClient()


# ---- retry behaviour -------------------------------------------------------
class _Boom(Exception):
    def __init__(self, code, msg="err"):
        super().__init__(f"{code} {msg}")
        self.code = code


def _client_with_script(monkeypatch, script, fallback=None):
    """script: list of outcomes per call; an Exception is raised, a str is returned."""
    _install_fake_genai(monkeypatch, "{}")
    # Keep the test independent of the developer's real .env / environment.
    monkeypatch.setitem(sys.modules, "dotenv", None)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    monkeypatch.delenv("GEMINI_FALLBACK_MODEL", raising=False)
    c = llm_client.GeminiClient(api_key="k", model="primary", fallback_model=fallback)
    c._sleep = lambda s: None
    calls = []

    def fake_generate(model, system, user):
        calls.append(model)
        out = script[min(len(calls) - 1, len(script) - 1)]
        if isinstance(out, Exception):
            raise out
        return out

    c._generate = fake_generate
    return c, calls


def test_retries_503_then_succeeds(monkeypatch):
    c, calls = _client_with_script(monkeypatch, [_Boom(503), _Boom(503), "OK"])
    assert c.complete("s", "u") == "OK"
    assert len(calls) == 3


def test_gives_up_after_max_retries(monkeypatch):
    c, calls = _client_with_script(monkeypatch, [_Boom(503)])
    with pytest.raises(_Boom):
        c.complete("s", "u")
    assert len(calls) == 4  # 1 try + 3 retries


def test_non_transient_error_not_retried(monkeypatch):
    c, calls = _client_with_script(monkeypatch, [_Boom(404, "NOT_FOUND")])
    with pytest.raises(_Boom):
        c.complete("s", "u")
    assert len(calls) == 1


def test_fallback_model_used_after_primary_fails(monkeypatch):
    c, calls = _client_with_script(
        monkeypatch, [_Boom(503), _Boom(503), _Boom(503), _Boom(503), "FROM_BACKUP"],
        fallback="backup")
    assert c.complete("s", "u") == "FROM_BACKUP"
    assert calls[-1] == "backup" and calls[0] == "primary"