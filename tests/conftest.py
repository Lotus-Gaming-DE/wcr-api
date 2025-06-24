import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


@pytest.fixture(scope="session", autouse=True)
def cleanup_logs(tmp_path_factory):
    yield
    log_dir = Path("logs")
    if log_dir.exists():
        shutil.rmtree(log_dir)
