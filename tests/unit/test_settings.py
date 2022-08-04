import pytest

from sonic.settings import Settings


@pytest.fixture(autouse=True)
def _reset_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SONIC_TELEMETRY__SERVICE", raising=False)
    monkeypatch.delenv("SONIC_TELEMETRY__HOST", raising=False)
    monkeypatch.delenv("SONIC_TELEMETRY__PORT", raising=False)


def test_TELEMETRY(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SONIC_TELEMETRY__SERVICE", "service")
    monkeypatch.setenv("SONIC_TELEMETRY__HOST", "jaeger")
    monkeypatch.setenv("SONIC_TELEMETRY__PORT", "3000")

    settings = Settings()

    assert settings.telemetry.service == "service"
    assert settings.telemetry.host == "jaeger"
    assert settings.telemetry.port == 3000
