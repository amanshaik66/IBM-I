from pathlib import PurePosixPath

from behavior_lab.models import Authority, Environment
from behavior_lab.runner import BehaviorLabController
from behavior_lab.transports.mock import MockTransport


def test_mock_is_permanently_non_authoritative() -> None:
    assert MockTransport().authority is Authority.NON_AUTHORITATIVE


def test_controller_workspace_and_cleanup() -> None:
    transport = MockTransport()
    environment = Environment(
        "res-mock-local",
        "mock",
        None,
        Authority.NON_AUTHORITATIVE,
        "RESMCK",
        PurePosixPath("/tmp/res-mock"),
        {"command": "mock"},
    )
    controller = BehaviorLabController(environment, transport)
    lease = controller.open_workspace("a1b2-extra")
    controller.cleanup(lease)
    assert lease.library == "RESMCKA1B2"
    assert transport.commands == [
        "CREATE RESMCKA1B2 /tmp/res-mock/a1b2",
        "CLEAN RESMCKA1B2 /tmp/res-mock/a1b2",
    ]
