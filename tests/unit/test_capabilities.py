from behavior_lab.capabilities import (
    Capability,
    CapabilityRequirement,
    CapabilityStatus,
    SchedulingDisposition,
    evaluate_capabilities,
)


def test_runnable_capabilities_are_not_a_semantic_result() -> None:
    decision = evaluate_capabilities(
        [CapabilityRequirement("compiler.rpgle")],
        [Capability("compiler.rpgle", CapabilityStatus.AVAILABLE, "7.5")],
    )
    assert decision.disposition is SchedulingDisposition.RUNNABLE


def test_missing_discovery_is_blocked() -> None:
    decision = evaluate_capabilities([CapabilityRequirement("sql.services")], [])
    assert decision.disposition is SchedulingDisposition.BLOCKED


def test_unavailable_is_distinct_from_failure() -> None:
    decision = evaluate_capabilities(
        [CapabilityRequirement("compiler.cobol")],
        [Capability("compiler.cobol", CapabilityStatus.UNAVAILABLE)],
    )
    assert decision.disposition is SchedulingDisposition.UNAVAILABLE
