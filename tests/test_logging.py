import logging
from importlib import reload

from app import logging as logging_mod


def test_log_level_from_env(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    reload(logging_mod)
    logging_mod.configure_logging()
    assert logging.getLogger().level == logging.DEBUG
