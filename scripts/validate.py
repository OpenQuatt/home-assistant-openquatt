#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
COMPANION_RAW = "https://raw.githubusercontent.com/OpenQuatt/home-assistant-openquatt/main/"

EXPECTED_TITLES = {
    "dashboards/duo-en.yaml": [
        "Overview", "Energy", "Flow", "Heat control", "Cooling", "HPs",
        "Sensor Configuration", "Tuning", "Service & Test", "Diagnostics",
    ],
    "dashboards/duo-nl.yaml": [
        "Overzicht", "Energie", "Flow", "Warmteregeling", "Koeling",
        "Warmtepompen", "Sensorconfiguratie", "Instellingen",
        "Service en test", "Diagnostiek",
    ],
    "dashboards/single-en.yaml": [
        "Overview", "Energy", "Flow", "Heat control", "Cooling", "HP1",
        "Sensor Configuration", "Tuning", "Service & Test", "Diagnostics",
    ],
    "dashboards/single-nl.yaml": [
        "Overzicht", "Energie", "Flow", "Warmteregeling", "Koeling", "HP1",
        "Sensorconfiguratie", "Instellingen", "Service en test", "Diagnostiek",
    ],
}

REQUIRED_FILES = {
    "assets/brand/openquatt-logo-horizontal-adaptive.svg",
    "assets/brand/openquatt-logo-horizontal-universal.svg",
    "assets/brand/openquatt-logo-horizontal-light.svg",
    "assets/brand/openquatt-logo-horizontal-dark.svg",
    "assets/brand/openquatt-logo-compact-dark.svg",
    "assets/brand/favicon.svg",
    "assets/brand/favicon-16x16.png",
    "assets/brand/favicon-32x32.png",
    "assets/brand/apple-touch-icon.png",
    "assets/brand/openquatt-social-card-1280x640.png",
    "assets/heatpump/Cool.png",
    "assets/heatpump/Heat.png",
    "assets/heatpump/Quatt.png",
    "packages/dynamic-cooling.yaml",
    "packages/dynamic-sources.yaml",
    "tools/quatt-insights-export/README.md",
    "tools/quatt-insights-export/openquatt_quatt_insights_export.py",
    "tools/quatt-insights-export/openquatt_quatt_insights_export.yaml",
}

DYNAMIC_SUPPLY_TARGET_PACKAGE_MARKERS = {
    "  openquatt_source_heating_supply_target:\n",
    "          - input_text.openquatt_source_heating_supply_target\n",
    "      - name: OpenQuatt Ext Heating Supply Target\n        unique_id: openquatt_ext_heating_supply_target\n",
    "      - name: OpenQuatt Ext Heating Supply Target Valid\n        unique_id: openquatt_ext_heating_supply_target_valid\n",
    "val >= 20 and val <= 70",
}

HA_INGRESS_HEARTBEAT_PACKAGE_MARKERS = {
    "      - name: OpenQuatt HA Ingress Heartbeat\n        unique_id: openquatt_ha_ingress_heartbeat\n",
    '"{{ (as_timestamp(now()) / 60) | int }}"',
}

DYNAMIC_SUPPLY_TARGET_DASHBOARD_MARKERS = {
    "select.openquatt_heating_supply_target_source",
    "sensor.openquatt_heating_supply_target_selected",
    "sensor.openquatt_heating_supply_target_source",
    "input_text.openquatt_source_heating_supply_target",
    "sensor.openquatt_ext_heating_supply_target",
    "binary_sensor.openquatt_ext_heating_supply_target_valid",
}

# Dashboard contract for the current OpenQuatt firmware generation.
# The standard dashboards intentionally use only firmware entities that are
# available in Home Assistant by default. Advanced entities that are
# disabled_by_default in firmware must stay out of the stock dashboards.
REQUIRED_FIRMWARE_DASHBOARD_MARKERS = {
    "number.openquatt_day_max_frequency",
    "number.openquatt_silent_max_frequency",
    "select.openquatt_cooling_restart_mode",
    "number.openquatt_cooling_minimum_off_time",
    "time.openquatt_cooling_schedule_start_time",
    "time.openquatt_cooling_schedule_end_time",
    "sensor.openquatt_cooling_start_block_reason",
    "sensor.openquatt_cooling_start_block_remaining",
    "sensor.openquatt_heating_electrical_energy_daily",
    "sensor.openquatt_cooling_electrical_energy_daily",
    "sensor.openquatt_heatpump_cooling_energy_daily",
    "sensor.openquatt_heatpump_eer_daily",
    "sensor.openquatt_heating_electrical_energy_cumulative",
    "sensor.openquatt_cooling_electrical_energy_cumulative",
    "sensor.openquatt_heatpump_cooling_energy_cumulative",
    "sensor.openquatt_heatpump_eer_cumulative",
    "sensor.openquatt_total_cooling_power",
    "sensor.openquatt_total_eer",
    "sensor.openquatt_cooling_effective_minimum_supply_temp",
    "sensor.openquatt_water_supply_temp_effective_source",
    "sensor.openquatt_water_supply_temperature_calibration_status",
    "binary_sensor.openquatt_water_supply_temperature_calibration_required",
    "binary_sensor.openquatt_water_supply_temp_fallback_active",
    "sensor.openquatt_ha_ingress_age",
    "binary_sensor.openquatt_ha_ingress_fresh",
    "switch.openquatt_auxiliary_heat_source_connected",
    "switch.openquatt_boiler_fallback_on_heat_pump_fault",
    "select.openquatt_boiler_connection",
    "binary_sensor.openquatt_otb_boiler_link_available",
    "binary_sensor.openquatt_otb_central_heating_active",
    "binary_sensor.openquatt_otb_flame_on",
    "sensor.openquatt_otb_ch_water_pressure",
    "sensor.openquatt_otb_boiler_water_temperature",
    "sensor.openquatt_otb_return_water_temperature",
    "sensor.openquatt_otb_domestic_hot_water_temperature",
    "sensor.openquatt_hp1_excluded_compressor_frequency_range",
}

DUO_FIRMWARE_DASHBOARD_MARKERS = {
    "sensor.openquatt_hp2_excluded_compressor_frequency_range",
}

DISALLOWED_DASHBOARD_ENTITIES = {
    # Removed legacy entities.
    "number.openquatt_day_max_level",
    "number.openquatt_silent_max_level",
    "sensor.openquatt_hp1_excluded_compressor_levels",
    "sensor.openquatt_hp2_excluded_compressor_levels",
    # Advanced firmware entities that are disabled_by_default.
    "number.openquatt_electrical_current_limit",
    "number.openquatt_hp1_excluded_frequency_minimum",
    "number.openquatt_hp1_excluded_frequency_maximum",
    "number.openquatt_hp2_excluded_frequency_minimum",
    "number.openquatt_hp2_excluded_frequency_maximum",
    "switch.openquatt_power_house_run_extension",
    "number.openquatt_power_house_run_extension_stop_margin",
    "sensor.openquatt_power_house_run_extension_status",
    "button.openquatt_reset_cumulative_energy_counters",
    "binary_sensor.openquatt_compressor_cycling_warning",
    "binary_sensor.openquatt_compressor_cycling_warning_2h",
    "binary_sensor.openquatt_compressor_cycling_warning_72h",
    "binary_sensor.openquatt_alternating_compressor_starts_warning",
}



def dashboard_titles(path: Path) -> list[str]:
    titles: list[str] = []
    pattern = re.compile(r"^\s*-\s+title:\s*(.+?)\s*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            titles.append(match.group(1).strip().strip("'").strip('"'))
    return titles


def markdown_links(path: Path) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8"))


def main() -> int:
    findings: list[str] = []

    for relative in sorted(REQUIRED_FILES):
        if not (ROOT / relative).is_file():
            findings.append(f"Missing required file: {relative}")

    for relative, expected in EXPECTED_TITLES.items():
        path = ROOT / relative
        if not path.is_file():
            findings.append(f"Missing dashboard: {relative}")
            continue
        actual = dashboard_titles(path)
        if actual != expected:
            findings.append(f"Unexpected view titles in {relative}: {actual}")

        text = path.read_text(encoding="utf-8")
        if "OpenQuatt/OpenQuatt/main/docs/dashboard" in text:
            findings.append(f"Legacy dashboard asset URL in {relative}")
        for asset in re.findall(re.escape(COMPANION_RAW) + r"([^\s\"']+)", text):
            if not (ROOT / asset).is_file():
                findings.append(f"Missing referenced asset in {relative}: {asset}")

        for marker in sorted(DYNAMIC_SUPPLY_TARGET_DASHBOARD_MARKERS):
            if marker not in text:
                findings.append(f"Missing heating supply target contract in {relative}: {marker}")

        for marker in sorted(REQUIRED_FIRMWARE_DASHBOARD_MARKERS):
            if marker not in text:
                findings.append(f"Missing current firmware dashboard entity in {relative}: {marker}")

        if relative.startswith("dashboards/duo-"):
            for marker in sorted(DUO_FIRMWARE_DASHBOARD_MARKERS):
                if marker not in text:
                    findings.append(f"Missing Duo firmware dashboard entity in {relative}: {marker}")

        for entity_id in sorted(DISALLOWED_DASHBOARD_ENTITIES):
            if entity_id in text:
                findings.append(f"Disallowed dashboard entity in {relative}: {entity_id}")

        if re.search(r"^      - type: conditional\\s*$", text, re.MULTILINE):
            findings.append(
                f"Invalid top-level conditional section in {relative}: "
                "use a grid section with visibility conditions"
            )

    dynamic_sources = (ROOT / "packages/dynamic-sources.yaml").read_text(encoding="utf-8")
    for marker in sorted(DYNAMIC_SUPPLY_TARGET_PACKAGE_MARKERS):
        if marker not in dynamic_sources:
            findings.append(f"Missing heating supply target contract in packages/dynamic-sources.yaml: {marker}")
    for marker in sorted(HA_INGRESS_HEARTBEAT_PACKAGE_MARKERS):
        if marker not in dynamic_sources:
            findings.append(f"Missing HA ingress heartbeat contract in packages/dynamic-sources.yaml: {marker}")
    if 'last_refresh: "{{ now()' in dynamic_sources:
        findings.append("Stale last_refresh keepalive in packages/dynamic-sources.yaml: use the HA ingress heartbeat")

    markdown_paths = [ROOT / "README.md", *(ROOT / "docs").glob("*.md")]
    markdown_paths.extend((ROOT / "tools").glob("**/*.md"))
    for path in markdown_paths:
        for target in markdown_links(path):
            if target.startswith(("http://", "https://", "#")):
                continue
            relative_target = target.split("#", 1)[0]
            if relative_target and not (path.parent / relative_target).resolve().is_file():
                findings.append(f"Broken local link in {path.relative_to(ROOT)}: {target}")

    if findings:
        print(f"Validation found {len(findings)} issue(s):")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Companion validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
