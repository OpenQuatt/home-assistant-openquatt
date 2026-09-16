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
    "assets/openquatt_logo.png",
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
