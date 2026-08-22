from orchestration.orchestrator import run
from safety.gate import authorize


def valid_context():
    return {
        "objective": "review an indoor service robot mission",
        "mission_reviewed": True,
        "navigation_reviewed": True,
        "perception_reviewed": True,
        "human_interaction_reviewed": True,
        "hazards_reviewed": True,
        "emergency_stop_verified": True,
        "privacy_reviewed": True,
        "cybersecurity_reviewed": True,
        "deployment_readiness_reviewed": True,
        "human_approval": True,
    }


def test_reference_run_never_actuates():
    result = run(valid_context())
    assert result["physical_actuation"] is False
    assert result["autonomous_deployment"] is False


def test_complete_review_can_release_analysis():
    assert run(valid_context())["release_allowed"] is True


def test_missing_human_approval_fails_closed():
    context = valid_context()
    context["human_approval"] = False
    assert run(context)["release_allowed"] is False


def test_robot_command_is_never_authorized():
    assert authorize("robot_command", valid_context())["allowed"] is False


def test_unresolved_hazard_blocks_release():
    context = valid_context()
    context["unresolved_high_risk_hazard"] = True
    assert run(context)["release_allowed"] is False


def test_high_perception_uncertainty_blocks_release():
    context = valid_context()
    context["perception_uncertainty_high"] = True
    assert run(context)["release_allowed"] is False


def test_unsafe_human_proximity_blocks_release():
    context = valid_context()
    context["unsafe_human_proximity"] = True
    assert run(context)["release_allowed"] is False


def test_privacy_or_cybersecurity_gap_blocks_release():
    context = valid_context()
    context["cybersecurity_gap"] = True
    assert run(context)["release_allowed"] is False
