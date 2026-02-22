from gen_agent.models.settings import deep_merge_dict


def test_deep_merge_dict_nested() -> None:
    base = {"retry": {"enabled": True, "maxRetries": 3}, "theme": "dark"}
    overrides = {"retry": {"maxRetries": 5}, "quietStartup": True}
    merged = deep_merge_dict(base, overrides)

    assert merged["retry"]["enabled"] is True
    assert merged["retry"]["maxRetries"] == 5
    assert merged["theme"] == "dark"
    assert merged["quietStartup"] is True
