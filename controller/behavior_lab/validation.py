"""Repository validation CLI."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from behavior_lab.metrics import build_report
from behavior_lab.schema_validation import Draft202012Validator, FormatChecker


class ValidationFailure(Exception):
    pass


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationFailure(f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationFailure(f"{path}: expected JSON object")
    return value


def _validate_files(root: Path, schema_name: str, paths: Iterable[Path]) -> list[dict[str, Any]]:
    schema = _load(root / "registry/schemas" / schema_name)
    validator = Draft202012Validator(
        schema, format_checker=FormatChecker() if FormatChecker else None
    )
    documents = []
    for path in sorted(paths):
        document = _load(path)
        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
        if errors:
            detail = "; ".join(
                f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}" for error in errors
            )
            raise ValidationFailure(f"{path}: {detail}")
        documents.append(document)
    return documents


def validate_registry(root: Path) -> None:
    cases = _validate_files(
        root, "coverage-case.schema.json", (root / "registry/coverage").glob("*.json")
    )
    releases = _validate_files(
        root, "release-support.schema.json", (root / "registry/releases").glob("*.json")
    )
    ids = [case["semantic_id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValidationFailure("duplicate semantic ID")
    known, release_ids = set(ids), {item["release_id"] for item in releases}
    for case in cases:
        filename = root / "registry/coverage" / f"{case['semantic_id']}.json"
        if not filename.exists():
            raise ValidationFailure(f"semantic ID/file mismatch: {case['semantic_id']}")
        missing = set(case["prerequisites"]) - known
        if missing:
            raise ValidationFailure(
                f"{case['semantic_id']}: missing prerequisites {sorted(missing)}"
            )
        missing_components = set(case["component_semantic_ids"]) - known
        if missing_components:
            raise ValidationFailure(
                f"{case['semantic_id']}: missing interaction components {sorted(missing_components)}"
            )
        if case["case_kind"] != "single_feature" and not case["component_semantic_ids"]:
            raise ValidationFailure(f"{case['semantic_id']}: interaction case requires components")
        if case["mutable_resources"] and not case["phases"]["cleanup_verification"].strip():
            raise ValidationFailure(
                f"{case['semantic_id']}: mutable resources require cleanup verification"
            )
        if case["expectation_governance"]["change_class"] == "semantic_change":
            if not case["expectation_governance"]["evidence_required"] or not case["evidence_refs"]:
                raise ValidationFailure(
                    f"{case['semantic_id']}: semantic expectation change requires evidence"
                )
        unknown_releases = set(case["applicability"]["release_ids"]) - release_ids
        if unknown_releases:
            raise ValidationFailure(
                f"{case['semantic_id']}: unknown releases {sorted(unknown_releases)}"
            )
        for fixture in case["fixtures"]["source"]:
            source_path = root / fixture
            if not source_path.is_file():
                raise ValidationFailure(f"{case['semantic_id']}: missing fixture {fixture}")
            if fixture.startswith("ibmi/"):
                if source_path.stem != source_path.stem.upper() or len(source_path.stem) > 10:
                    raise ValidationFailure(
                        f"{case['semantic_id']}: invalid IBM i source name {fixture}"
                    )
                if "UNVERIFIED ON IBM i" not in source_path.read_text():
                    raise ValidationFailure(
                        f"{case['semantic_id']}: source lacks verification warning {fixture}"
                    )
        if (
            case["verification_status"]
            in {
                "compiled_on_ibmi",
                "executed_on_ibmi",
                "behavior_verified_on_ibmi",
                "integration_verified",
            }
            and not case["evidence_refs"]
        ):
            raise ValidationFailure(f"{case['semantic_id']}: IBM i status requires evidence")


def validate_tasks(root: Path) -> None:
    tasks = _validate_files(
        root, "task-contract.schema.json", (root / "agents/tasks").glob("*.json")
    )
    case_ids = {p.stem for p in (root / "registry/coverage").glob("*.json")}
    for task in tasks:
        if task["semantic_id"] not in case_ids:
            raise ValidationFailure(f"{task['task_id']}: unknown semantic ID")
        if task["task_id"] != f"TASK-{task['semantic_id']}":
            raise ValidationFailure(f"{task['task_id']}: task and semantic IDs differ")
        if task["change_scope"] == "implementation_only":
            forbidden = " ".join(task["forbidden_changes"]).lower()
            if "semantic" not in forbidden and "expected" not in forbidden:
                raise ValidationFailure(
                    f"{task['task_id']}: implementation task must forbid semantic expectation changes"
                )
        if (
            task["assigned_role"] == "implementer"
            and task["independent_review"]["implementer_may_self_approve"]
        ):
            raise ValidationFailure(f"{task['task_id']}: implementer cannot self-approve")
        components, workflows, taxonomy, _, _ = load_estate_catalogs(root)
        known_components = {item["component_id"] for item in components["components"]}
        known_workflows = {item["workflow_id"] for item in workflows["workflows"]}
        known_capabilities = {item["capability_id"] for item in taxonomy["capabilities"]}
        if (
            set(task["component_ids"]) - known_components
            or set(task["workflow_ids"]) - known_workflows
            or set(task["capability_ids"]) - known_capabilities
        ):
            raise ValidationFailure(f"{task['task_id']}: task has invalid RES blueprint references")


def _assert_acyclic(nodes: dict[str, list[str]], label: str) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise ValidationFailure(f"{label}: dependency cycle at {node}")
        if node in visited:
            return
        visiting.add(node)
        for dependency in nodes[node]:
            if dependency not in nodes:
                raise ValidationFailure(f"{label}: unknown prerequisite node {dependency}")
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for node in nodes:
        visit(node)


def validate_architecture(root: Path) -> None:
    for schema_path in sorted((root / "registry/schemas").glob("*.json")):
        schema = _load(schema_path)
        check_schema = getattr(Draft202012Validator, "check_schema", None)
        if check_schema is not None:
            try:
                check_schema(schema)
            except Exception as exc:
                raise ValidationFailure(f"{schema_path}: invalid JSON Schema: {exc}") from exc
    builds = _validate_files(
        root, "build-manifest.schema.json", (root / "registry/builds").glob("*.json")
    )
    case_ids = {path.stem for path in (root / "registry/coverage").glob("*.json")}
    for build in builds:
        unknown = set(build["semantic_case_ids"]) - case_ids
        if unknown:
            raise ValidationFailure(
                f"{build['manifest_id']}: unknown semantic cases {sorted(unknown)}"
            )
        graph = {node["node_id"]: node["prerequisite_nodes"] for node in build["nodes"]}
        if len(graph) != len(build["nodes"]):
            raise ValidationFailure(f"{build['manifest_id']}: duplicate build node")
        _assert_acyclic(graph, build["manifest_id"])
        for node in build["nodes"]:
            if (
                node["source_kind"] in {"source_less", "vendor_black_box"}
                and node["source"] is not None
            ):
                raise ValidationFailure(
                    f"{node['node_id']}: source-less object must not claim source"
                )
            if node["source_kind"] in {"stream_file", "source_member"}:
                if node["source"] is None or not (root / node["source"]["path"]).is_file():
                    raise ValidationFailure(f"{node['node_id']}: source path is missing")
    graphs = _validate_files(
        root, "dependency-graph.schema.json", (root / "registry/dependencies").glob("*.json")
    )
    for graph in graphs:
        node_ids = {node["id"] for node in graph["nodes"]}
        for edge in graph["edges"]:
            if edge["from"] not in node_ids or (
                edge["to"] is not None and edge["to"] not in node_ids
            ):
                raise ValidationFailure(
                    f"{graph['graph_id']}: dependency edge references unknown node"
                )
    _validate_files(
        root, "comparison-policy.schema.json", (root / "registry/policies").glob("*.json")
    )
    _validate_files(root, "baseline.schema.json", (root / "registry/baselines").glob("*.json"))
    _validate_files(
        root, "runtime-observation.schema.json", (root / "registry/observations").glob("*.json")
    )
    _validate_files(
        root, "workflow.schema.json", [root / "registry/workflows/golden-workflows.json"]
    )
    _validate_files(
        root, "security-personas.schema.json", [root / "registry/personas/security-personas.json"]
    )
    _validate_files(
        root, "simulator-contract.schema.json", [root / "registry/simulators/contracts.json"]
    )


def load_estate_catalogs(
    root: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    components = _validate_files(
        root, "res-component-catalog.schema.json", [root / "registry/estate/components.json"]
    )[0]
    workflows = _validate_files(
        root, "res-workflow-catalog.schema.json", [root / "registry/estate/workflows.json"]
    )[0]
    taxonomy = _validate_files(
        root, "capability-taxonomy.schema.json", [root / "registry/capabilities/taxonomy.json"]
    )[0]
    allocations = _validate_files(
        root, "capability-allocation.schema.json", [root / "registry/capabilities/allocations.json"]
    )[0]
    trace = _validate_files(
        root,
        "business-semantic-trace.schema.json",
        [root / "registry/traceability/business-semantic.json"],
    )[0]
    return components, workflows, taxonomy, allocations, trace


def estate_gap_report(root: Path) -> dict[str, Any]:
    components, workflows, taxonomy, allocations, _ = load_estate_catalogs(root)
    component_ids = {item["component_id"] for item in components["components"]}
    workflow_ids = {item["workflow_id"] for item in workflows["workflows"]}
    semantic_ids = {path.stem for path in (root / "registry/coverage").glob("*.json")}
    taxonomy_ids = {item["capability_id"] for item in taxonomy["capabilities"]}
    by_capability = {item["capability_id"]: item for item in allocations["allocations"]}
    unallocated = sorted(taxonomy_ids - set(by_capability))
    semantic_gaps: list[dict[str, str]] = []
    for workflow in workflows["workflows"]:
        for capability_id in workflow["platform_capabilities"]:
            allocation = by_capability.get(capability_id)
            if allocation is None or not allocation["semantic_families"]:
                semantic_gaps.append(
                    {"workflow_id": workflow["workflow_id"], "capability_id": capability_id}
                )
    invalid_allocation_refs = sorted(
        {
            reference
            for item in allocations["allocations"]
            for reference in item["workflow_ids"]
            if reference not in workflow_ids
        }
        | {
            reference
            for item in allocations["allocations"]
            for reference in item["component_ids"]
            if reference not in component_ids
        }
        | {
            reference
            for item in allocations["allocations"]
            for reference in item["semantic_case_ids"]
            if reference not in semantic_ids
        }
    )
    placements = Counter(item["placement"] for item in allocations["allocations"])
    return {
        "taxonomy_status": taxonomy["completeness"],
        "component_count": len(component_ids),
        "workflow_count": len(workflow_ids),
        "capability_count": len(taxonomy_ids),
        "allocation_count": len(by_capability),
        "placements": dict(sorted(placements.items())),
        "unallocated_capabilities": unallocated,
        "semantic_coverage_gaps": semantic_gaps,
        "invalid_allocation_references": invalid_allocation_refs,
        "warning": "The seed taxonomy is explicitly partial; zero gaps is not complete IBM i coverage.",
    }


def validate_estate(root: Path) -> None:
    components, workflows, taxonomy, allocations, trace = load_estate_catalogs(root)
    component_ids = [item["component_id"] for item in components["components"]]
    workflow_ids = [item["workflow_id"] for item in workflows["workflows"]]
    taxonomy_ids = [item["capability_id"] for item in taxonomy["capabilities"]]
    allocation_ids = [item["capability_id"] for item in allocations["allocations"]]
    for label, values in (
        ("component", component_ids),
        ("workflow", workflow_ids),
        ("capability", taxonomy_ids),
        ("allocation", allocation_ids),
    ):
        if len(values) != len(set(values)):
            raise ValidationFailure(f"duplicate RES {label} ID")
    known_components, known_workflows = set(component_ids), set(workflow_ids)
    known_capabilities = set(taxonomy_ids)
    semantic_ids = {path.stem for path in (root / "registry/coverage").glob("*.json")}
    for component in components["components"]:
        missing = set(component["depends_on"]) - known_components
        if missing:
            raise ValidationFailure(
                f"{component['component_id']}: unknown component dependencies {sorted(missing)}"
            )
    _assert_acyclic(
        {item["component_id"]: item["depends_on"] for item in components["components"]},
        "RES component graph",
    )
    for workflow in workflows["workflows"]:
        missing_components = set(workflow["components"]) - known_components
        missing_capabilities = set(workflow["platform_capabilities"]) - known_capabilities
        missing_cases = set(workflow["semantic_case_ids"]) - semantic_ids
        if missing_components or missing_capabilities or missing_cases:
            raise ValidationFailure(
                f"{workflow['workflow_id']}: invalid references components={sorted(missing_components)} "
                f"capabilities={sorted(missing_capabilities)} cases={sorted(missing_cases)}"
            )
    report = estate_gap_report(root)
    if report["unallocated_capabilities"]:
        raise ValidationFailure(f"UNALLOCATED CAPABILITY: {report['unallocated_capabilities']}")
    if report["semantic_coverage_gaps"]:
        raise ValidationFailure(f"SEMANTIC COVERAGE GAP: {report['semantic_coverage_gaps']}")
    if report["invalid_allocation_references"]:
        raise ValidationFailure(
            f"invalid capability allocation references: {report['invalid_allocation_references']}"
        )
    if set(allocation_ids) - known_capabilities:
        raise ValidationFailure("allocation references capability outside taxonomy")
    for item in allocations["allocations"]:
        if item["placement"] != "semantic_edge" and not item["workflow_ids"]:
            raise ValidationFailure(
                f"{item['capability_id']}: integrated placement requires workflow"
            )
        if item["placement"] == "semantic_edge" and item["workflow_ids"]:
            raise ValidationFailure(
                f"{item['capability_id']}: semantic edge must not pollute workflows"
            )
    semantic_links = {item["semantic_id"]: item for item in trace["semantic_links"]}
    workflow_links = {item["workflow_id"]: item for item in trace["workflow_links"]}
    if set(semantic_links) != semantic_ids:
        raise ValidationFailure(
            "semantic traceability must cover every current semantic case exactly"
        )
    if set(workflow_links) != known_workflows:
        raise ValidationFailure("workflow traceability must cover every workflow exactly")
    for item in semantic_links.values():
        if (
            set(item["capability_ids"]) - known_capabilities
            or set(item["component_ids"]) - known_components
            or set(item["workflow_ids"]) - known_workflows
        ):
            raise ValidationFailure(f"{item['semantic_id']}: broken business-to-semantic trace")
    workflows_by_id = {item["workflow_id"]: item for item in workflows["workflows"]}
    for workflow_id, item in workflow_links.items():
        workflow = workflows_by_id[workflow_id]
        if set(item["component_ids"]) != set(workflow["components"]):
            raise ValidationFailure(f"{workflow_id}: trace component set differs from workflow")
        if set(item["capability_ids"]) != set(workflow["platform_capabilities"]):
            raise ValidationFailure(f"{workflow_id}: trace capability set differs from workflow")


def validate_manifests(root: Path) -> None:
    _validate_files(root, "manifest.schema.json", [root / "manifests/res-modules.json"])
    environments = _validate_files(
        root, "environment.schema.json", (root / "manifests").glob("environment.*.json")
    )
    for environment in environments:
        if environment["kind"] == "mock" and environment["authority"] != "non_authoritative":
            raise ValidationFailure("mock environment cannot be authoritative")


def run(root: Path, target: str) -> None:
    actions = {
        "registry": validate_registry,
        "tasks": validate_tasks,
        "manifests": validate_manifests,
        "architecture": validate_architecture,
        "estate": validate_estate,
    }
    selected = actions.values() if target == "all" else [actions[target]]
    for action in selected:
        action(root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the RES repository")
    parser.add_argument(
        "target",
        choices=[
            "all",
            "registry",
            "tasks",
            "manifests",
            "architecture",
            "estate",
            "report",
            "estate-report",
        ],
        nargs="?",
        default="all",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        if args.target == "estate-report":
            print(json.dumps(estate_gap_report(args.root.resolve()), indent=2))
            return 0
        if args.target == "report":
            root = args.root.resolve()
            cases = [_load(path) for path in sorted((root / "registry/coverage").glob("*.json"))]
            releases = [
                _load(path)["release_id"]
                for path in sorted((root / "registry/releases").glob("*.json"))
            ]
            print(json.dumps(build_report(cases, releases), indent=2))
            return 0
        run(args.root.resolve(), args.target)
    except ValidationFailure as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"validated {args.target}: {args.root.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
