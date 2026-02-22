from pathlib import Path

from gen_agent.models.schema_export import export_schemas


def test_export_schemas(tmp_path: Path) -> None:
    files = export_schemas(tmp_path)
    assert files
    assert (tmp_path / "AgentMessage.schema.json").exists()
    assert (tmp_path / "SettingsModel.schema.json").exists()
