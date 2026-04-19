from pathlib import Path
import yaml

from nexteco.model import load_yaml, render_markdown, validate_cost_model


def test_full_example_is_structurally_valid():
    data = load_yaml(Path("cost_of_running.full.yaml.example"))
    result = validate_cost_model(data)
    assert result.is_valid()


def test_render_contains_expected_sections():
    data = load_yaml(Path("cost_of_running.min.yaml.example"))
    markdown = render_markdown(data)
    assert "# Cost of Running" in markdown
    assert "## Canonical unit of work" in markdown
    assert "## Scenarios" in markdown


def test_total_cost_arithmetic_check():
    data = {
        "date_updated": "2026-04-19",
        "canonical_unit_of_work": {
            "name": "one request",
            "status": "estimated",
        },
        "deployment": {"provider": "local"},
        "scenario": {
            "name": "default",
            "runtime_seconds": {"value": 2.0, "status": "estimated"},
            "local_compute": {
                "energy_kwh": {"value": 0.001, "status": "estimated"},
                "electricity_cost_usd": {"value": 0.2, "status": "estimated"},
                "carbon_gco2e": {"value": 0.3, "status": "estimated"},
            },
            "external_api_cost_usd": {"value": 0.4, "status": "estimated"},
            "totals": {
                "total_cost_usd": {"value": 0.6, "status": "estimated"},
                "total_carbon_gco2e": {"value": 0.3, "status": "estimated"},
            },
        },
    }
    result = validate_cost_model(data)
    assert result.is_valid()


def test_total_cost_arithmetic_failure_is_detected():
    data = {
        "date_updated": "2026-04-19",
        "canonical_unit_of_work": {
            "name": "one request",
            "status": "estimated",
        },
        "deployment": {"provider": "local"},
        "scenario": {
            "name": "default",
            "runtime_seconds": {"value": 2.0, "status": "estimated"},
            "local_compute": {
                "energy_kwh": {"value": 0.001, "status": "estimated"},
                "electricity_cost_usd": {"value": 0.2, "status": "estimated"},
                "carbon_gco2e": {"value": 0.3, "status": "estimated"},
            },
            "external_api_cost_usd": {"value": 0.4, "status": "estimated"},
            "totals": {
                "total_cost_usd": {"value": 0.5, "status": "estimated"},
                "total_carbon_gco2e": {"value": 0.3, "status": "estimated"},
            },
        },
    }
    result = validate_cost_model(data)
    assert not result.is_valid()
    assert any("total_cost_usd" in issue.message for issue in result.errors)
