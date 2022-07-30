import pytest

from sonic.settings import Settings


@pytest.fixture(autouse=True)
def _reset_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SONIC_JAEGER__SERVICE", raising=False)
    monkeypatch.delenv("SONIC_JAEGER__HOST", raising=False)
    monkeypatch.delenv("SONIC_JAEGER__PORT", raising=False)


def test_jaeger(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SONIC_JAEGER__SERVICE", "service")
    monkeypatch.setenv("SONIC_JAEGER__HOST", "jaeger")
    monkeypatch.setenv("SONIC_JAEGER__PORT", "3000")

    settings = Settings()

    assert settings.jaeger.service == "service"
    assert settings.jaeger.host == "jaeger"
    assert settings.jaeger.port == 3000
