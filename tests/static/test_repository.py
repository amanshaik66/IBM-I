from pathlib import Path

from behavior_lab.validation import run

ROOT = Path(__file__).parents[2]


def test_all_machine_readable_artifacts() -> None:
    run(ROOT, "all")


def test_exactly_ten_foundation_cases() -> None:
    assert len(list((ROOT / "registry/coverage").glob("*.json"))) == 10


def test_ibmi_sources_are_explicitly_unverified() -> None:
    sources = [path for path in (ROOT / "ibmi").rglob("*") if path.is_file()]
    assert sources
    for source in sources:
        assert "UNVERIFIED ON IBM i" in source.read_text(), source


def test_hardening_models_are_present() -> None:
    required = {
        "artifact.schema.json",
        "baseline.schema.json",
        "build-manifest.schema.json",
        "comparison-policy.schema.json",
        "dependency-graph.schema.json",
        "object-provenance.schema.json",
        "runtime-observation.schema.json",
    }
    assert required <= {path.name for path in (ROOT / "registry/schemas").glob("*.json")}


def test_candidate_releases_include_74_through_76() -> None:
    releases = {path.stem for path in (ROOT / "registry/releases").glob("*.json")}
    assert {"ibmi-7.4", "ibmi-7.5", "ibmi-7.6"} <= releases


def test_res_blueprint_catalogs_exist() -> None:
    required = [
        ROOT / "registry/estate/components.json",
        ROOT / "registry/estate/workflows.json",
        ROOT / "registry/capabilities/taxonomy.json",
        ROOT / "registry/capabilities/allocations.json",
        ROOT / "registry/traceability/business-semantic.json",
    ]
    assert all(path.is_file() for path in required)
