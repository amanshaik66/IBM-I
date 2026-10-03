from pathlib import Path

from behavior_lab.validation import estate_gap_report, run

ROOT = Path(__file__).parents[2]


def test_estate_catalogs_are_referentially_complete() -> None:
    run(ROOT, "estate")


def test_seed_taxonomy_is_fully_allocated_but_explicitly_partial() -> None:
    report = estate_gap_report(ROOT)
    assert report["taxonomy_status"] == "partial_seed_taxonomy"
    assert report["component_count"] == 37
    assert report["workflow_count"] == 23
    assert report["capability_count"] == 49
    assert report["unallocated_capabilities"] == []
    assert report["semantic_coverage_gaps"] == []
    assert report["placements"] == {
        "business_integrated": 36,
        "operations_integrated": 11,
        "semantic_edge": 2,
    }
