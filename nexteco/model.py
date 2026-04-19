from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any
import math
import yaml


ALLOWED_STATUSES = {"measured", "estimated", "placeholder", "TODO"}


@dataclass
class ValidationIssue:
    level: str
    message: str


@dataclass
class ValidationResult:
    issues: list[ValidationIssue] = field(default_factory=list)

    def add(self, level: str, message: str) -> None:
        self.issues.append(ValidationIssue(level=level, message=message))

    @property
    def errors(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.level == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.level == "warning"]

    def is_valid(self) -> bool:
        return not self.errors


def load_yaml(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError("Top-level YAML must be a mapping.")
    return data


def write_text(path: str | Path, content: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _status_of(obj: Any) -> str | None:
    if isinstance(obj, dict):
        status = obj.get("status")
        if status is None:
            return None
        return str(status)
    return None


def _value_of(obj: Any) -> Any:
    if isinstance(obj, dict) and "value" in obj:
        return obj.get("value")
    return obj


def _check_status(result: ValidationResult, obj: Any, label: str) -> None:
    status = _status_of(obj)
    if status is None:
        result.add("warning", f"{label} is missing a status field.")
        return
    if status not in ALLOWED_STATUSES:
        result.add("error", f"{label} has invalid status '{status}'.")


def _check_date_string(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except Exception:
        return False


def _days_since(date_str: str) -> int | None:
    if not _check_date_string(date_str):
        return None
    then = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (date.today() - then).days


def validate_cost_model(data: dict[str, Any]) -> ValidationResult:
    result = ValidationResult()

    for field_name in ["date_updated", "canonical_unit_of_work", "deployment"]:
        if field_name not in data:
            result.add("error", f"Missing required top-level field: {field_name}")

    cuow = data.get("canonical_unit_of_work", {})
    if isinstance(cuow, dict):
        if not cuow.get("name"):
            result.add("error", "canonical_unit_of_work.name is required")
        _check_status(result, cuow, "canonical_unit_of_work")
    else:
        result.add("error", "canonical_unit_of_work must be a mapping")

    assumptions = data.get("assumptions", {})
    if assumptions and isinstance(assumptions, dict):
        for key, value in assumptions.items():
            if isinstance(value, dict) and ("value" in value or "status" in value):
                _check_status(result, value, f"assumptions.{key}")
                retrieved_date = value.get("retrieved_date")
                source_url = value.get("source_url")
                if retrieved_date is not None:
                    retrieved_date_str = str(retrieved_date)
                    if retrieved_date_str == "YYYY-MM-DD":
                        result.add("warning", f"assumptions.{key}.retrieved_date is still a template placeholder.")
                    elif not _check_date_string(retrieved_date_str):
                        result.add("error", f"assumptions.{key}.retrieved_date must be YYYY-MM-DD")
                    else:
                        age = _days_since(retrieved_date_str)
                        if age is not None and age > 90:
                            result.add(
                                "warning",
                                f"assumptions.{key} pricing/provenance data is older than 90 days; verify freshness.",
                            )
                if source_url is not None and source_url == "TODO":
                    result.add("warning", f"assumptions.{key}.source_url still needs human verification.")

    pricing = data.get("pricing", {})
    if pricing and isinstance(pricing, dict):
        external_apis = pricing.get("external_apis", [])
        if not isinstance(external_apis, list):
            result.add("error", "pricing.external_apis must be a list")
        else:
            for idx, api in enumerate(external_apis):
                if not isinstance(api, dict):
                    result.add("error", f"pricing.external_apis[{idx}] must be a mapping")
                    continue
                price_per_unit = api.get("price_per_unit", {})
                usage_per_unit = api.get("usage_per_canonical_unit", {})
                subtotal = api.get("subtotal_usd", {})
                _check_status(result, price_per_unit, f"pricing.external_apis[{idx}].price_per_unit")
                _check_status(result, usage_per_unit, f"pricing.external_apis[{idx}].usage_per_canonical_unit")
                _check_status(result, subtotal, f"pricing.external_apis[{idx}].subtotal_usd")
                source_url = price_per_unit.get("source_url")
                retrieved_date = price_per_unit.get("retrieved_date")
                if source_url in (None, "", "TODO"):
                    result.add("warning", f"pricing.external_apis[{idx}].price_per_unit.source_url should be set.")
                if retrieved_date:
                    retrieved_date_str = str(retrieved_date)
                    if retrieved_date_str == "YYYY-MM-DD":
                        result.add("warning", f"pricing.external_apis[{idx}].price_per_unit.retrieved_date is still a template placeholder.")
                    elif not _check_date_string(retrieved_date_str):
                        result.add("error", f"pricing.external_apis[{idx}].price_per_unit.retrieved_date must be YYYY-MM-DD")
                    else:
                        age = _days_since(retrieved_date_str)
                        if age is not None and age > 90:
                            result.add(
                                "warning",
                                f"pricing.external_apis[{idx}] pricing metadata is older than 90 days; verify freshness.",
                            )

                price_value = _value_of(price_per_unit)
                usage_value = _value_of(usage_per_unit)
                subtotal_value = _value_of(subtotal)
                if _is_number(price_value) and _is_number(usage_value) and _is_number(subtotal_value):
                    expected = float(price_value) * float(usage_value)
                    if not math.isclose(float(subtotal_value), expected, rel_tol=1e-9, abs_tol=1e-9):
                        result.add(
                            "error",
                            f"pricing.external_apis[{idx}].subtotal_usd does not match price_per_unit × usage_per_canonical_unit",
                        )

    scenarios = []
    if "scenario" in data:
        scenarios = [data["scenario"]]
    elif "scenarios" in data:
        scenarios = data["scenarios"]

    if not scenarios:
        result.add("error", "A model must define either 'scenario' or 'scenarios'.")
    if not isinstance(scenarios, list):
        result.add("error", "Scenarios must be represented as a list after normalization.")
        return result

    for idx, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            result.add("error", f"scenario[{idx}] must be a mapping")
            continue

        runtime = scenario.get("runtime_seconds", {})
        _check_status(result, runtime, f"scenario[{idx}].runtime_seconds")

        local_compute = scenario.get("local_compute", {})
        if isinstance(local_compute, dict):
            energy = local_compute.get("energy_kwh", {})
            elec_cost = local_compute.get("electricity_cost_usd", {})
            carbon = local_compute.get("carbon_gco2e", {})
            _check_status(result, energy, f"scenario[{idx}].local_compute.energy_kwh")
            _check_status(result, elec_cost, f"scenario[{idx}].local_compute.electricity_cost_usd")
            _check_status(result, carbon, f"scenario[{idx}].local_compute.carbon_gco2e")

        external_api_cost = scenario.get("external_api_cost_usd", {})
        _check_status(result, external_api_cost, f"scenario[{idx}].external_api_cost_usd")

        totals = scenario.get("totals", {})
        if isinstance(totals, dict):
            total_cost = totals.get("total_cost_usd", {})
            total_carbon = totals.get("total_carbon_gco2e", {})
            _check_status(result, total_cost, f"scenario[{idx}].totals.total_cost_usd")
            _check_status(result, total_carbon, f"scenario[{idx}].totals.total_carbon_gco2e")

            local_cost_value = _value_of(local_compute.get("electricity_cost_usd", {})) if isinstance(local_compute, dict) else None
            api_cost_value = _value_of(external_api_cost)
            total_cost_value = _value_of(total_cost)
            if _is_number(local_cost_value) and _is_number(api_cost_value) and _is_number(total_cost_value):
                expected = float(local_cost_value) + float(api_cost_value)
                if not math.isclose(float(total_cost_value), expected, rel_tol=1e-9, abs_tol=1e-9):
                    result.add("error", f"scenario[{idx}].totals.total_cost_usd does not equal local + external API cost")

            local_carbon_value = _value_of(local_compute.get("carbon_gco2e", {})) if isinstance(local_compute, dict) else None
            total_carbon_value = _value_of(total_carbon)
            if _is_number(local_carbon_value) and _is_number(total_carbon_value):
                if float(total_carbon_value) < float(local_carbon_value):
                    result.add("error", f"scenario[{idx}].totals.total_carbon_gco2e cannot be smaller than local carbon")

    return result


def normalize_scenarios(data: dict[str, Any]) -> list[dict[str, Any]]:
    if "scenarios" in data and isinstance(data["scenarios"], list):
        return data["scenarios"]
    if "scenario" in data and isinstance(data["scenario"], dict):
        return [data["scenario"]]
    return []


def render_markdown(data: dict[str, Any]) -> str:
    scenarios = normalize_scenarios(data)
    lines: list[str] = []
    lines.append("# Cost of Running")
    lines.append("")
    lines.append(f"- Date updated: `{data.get('date_updated', 'unknown')}`")
    lines.append("")

    cuow = data.get("canonical_unit_of_work", {})
    lines.append("## Canonical unit of work")
    lines.append("")
    lines.append(f"- Name: **{cuow.get('name', 'unknown')}**")
    if cuow.get("description"):
        lines.append(f"- Description: {cuow.get('description')}")
    if cuow.get("status"):
        lines.append(f"- Status: `{cuow.get('status')}`")
    notes = cuow.get("notes")
    if notes:
        lines.append(f"- Notes: {notes}")
    out_of_scope = cuow.get("out_of_scope", [])
    if out_of_scope:
        lines.append("- Out of scope:")
        for item in out_of_scope:
            lines.append(f"  - {item}")
    lines.append("")

    deployment = data.get("deployment", {})
    lines.append("## Deployment context")
    lines.append("")
    for key, value in deployment.items():
        lines.append(f"- {key.replace('_', ' ').capitalize()}: {value}")
    lines.append("")

    assumptions = data.get("assumptions", {})
    if assumptions:
        lines.append("## Assumptions")
        lines.append("")
        for key, value in assumptions.items():
            lines.append(f"### {key}")
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    lines.append(f"- {subkey}: {subvalue}")
            else:
                lines.append(f"- value: {value}")
            lines.append("")
    pricing = data.get("pricing", {})
    external_apis = pricing.get("external_apis", []) if isinstance(pricing, dict) else []
    if external_apis:
        lines.append("## External API pricing")
        lines.append("")
        for api in external_apis:
            lines.append(f"### {api.get('name', 'unknown-api')}")
            for key, value in api.items():
                if key == "name":
                    continue
                lines.append(f"- {key}: {value}")
            lines.append("")

    lines.append("## Scenarios")
    lines.append("")
    for scenario in scenarios:
        lines.append(f"### {scenario.get('name', 'unnamed')}")
        if scenario.get("description"):
            lines.append(f"- Description: {scenario.get('description')}")
        runtime = scenario.get("runtime_seconds", {})
        lines.append(f"- Runtime seconds: {runtime}")
        local_compute = scenario.get("local_compute", {})
        lines.append(f"- Local compute: {local_compute}")
        lines.append(f"- External API cost USD: {scenario.get('external_api_cost_usd', {})}")
        lines.append(f"- Totals: {scenario.get('totals', {})}")
        lines.append("")

    exclusions = data.get("exclusions", [])
    if exclusions:
        lines.append("## Exclusions")
        lines.append("")
        for item in exclusions:
            lines.append(f"- {item}")
        lines.append("")

    output_expectations = data.get("output_expectations", {})
    if output_expectations:
        lines.append("## Output expectations")
        lines.append("")
        for key, value in output_expectations.items():
            lines.append(f"- {key}: {value}")
        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("- Generated by NextEco.")
    lines.append("- The YAML file remains the source of truth.")
    lines.append("- Re-run `nexteco validate` and `nexteco render` after edits.")
    lines.append("")
    return "\n".join(lines)
