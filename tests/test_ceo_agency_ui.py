import importlib.util
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "examples" / "ceo_agency_ui.py"

spec = importlib.util.spec_from_file_location("ceo_agency_ui", MODULE_PATH)
ceo_agency_ui = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ceo_agency_ui
spec.loader.exec_module(ceo_agency_ui)


def test_load_config_uses_production_defaults_when_file_is_missing(tmp_path):
    config = ceo_agency_ui.load_config(tmp_path / "missing.json")

    assert config.model == ceo_agency_ui.DEFAULT_MODEL
    assert config.agents[0].name == "CEO"
    assert "production agency workspace" in config.shared_instructions
    assert any(agent.name == "AgentTrainer" for agent in config.agents)


def test_add_agent_persists_sanitized_custom_agent(tmp_path):
    config_path = tmp_path / "studio.json"
    settings_path = tmp_path / "assistants.json"
    studio = ceo_agency_ui.AgencyStudio(
        config_path=config_path, settings_path=settings_path
    )

    rows = studio.add_agent(
        "  Sales Ops!!  ",
        "Builds sales operations playbooks.",
        "Create CRM stages, sales scripts, forecasts, and handoff rules.",
        "gpt-5.2",
    )

    assert rows[-1][0] == "Sales Ops"
    saved = ceo_agency_ui.load_config(config_path)
    assert saved.agents[-1].name == "Sales Ops"
    assert saved.agents[-1].model == "gpt-5.2"


def test_add_agent_rejects_duplicate_ceo(tmp_path):
    studio = ceo_agency_ui.AgencyStudio(
        config_path=tmp_path / "studio.json",
        settings_path=tmp_path / "assistants.json",
    )

    with pytest.raises(ValueError, match="CEO already exists"):
        studio.add_agent("CEO", "Replacement", "Replace the CEO.")
