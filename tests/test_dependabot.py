import yaml
from pathlib import Path


def test_dependabot_config_valid():
    cfg_path = Path(".github/dependabot.yml")
    assert cfg_path.exists(), "dependabot config missing"
    with cfg_path.open() as f:
        data = yaml.safe_load(f)
    assert data["version"] == 2
    ecosystems = {u["package-ecosystem"] for u in data.get("updates", [])}
    assert {"pip", "github-actions"} <= ecosystems
