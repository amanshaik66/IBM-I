import json
from pathlib import Path

from behavior_lab.metrics import build_report

ROOT = Path(__file__).parents[2]


def test_report_is_multidimensional_and_never_claims_global_coverage() -> None:
    cases = [json.loads(path.read_text()) for path in (ROOT / "registry/coverage").glob("*.json")]
    report = build_report(cases, ["IBMI-7.4", "IBMI-7.5", "IBMI-7.6"])
    assert report["total_specified_cases"] == 10
    assert "percentage" not in report
    assert report["lacking_authoritative_evidence"] == 10
