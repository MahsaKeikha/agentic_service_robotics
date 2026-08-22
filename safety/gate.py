"""Fail-closed governance for F72 service robotics."""

BLOCKED_ACTIONS = {
    "robot_command",
    "actuate",
    "physical_actuation",
    "safety_override",
    "autonomous_deployment",
    "autonomous_door_or_elevator_control",
}

REQUIRED_REVIEWS = (
    "mission_reviewed",
    "navigation_reviewed",
    "perception_reviewed",
    "human_interaction_reviewed",
    "hazards_reviewed",
    "emergency_stop_verified",
    "privacy_reviewed",
    "cybersecurity_reviewed",
    "deployment_readiness_reviewed",
    "human_approval",
)


def authorize(action: str, context: dict | None = None) -> dict:
    """Authorize analysis-only work and fail closed on consequential execution."""
    context = context or {}
    if action in BLOCKED_ACTIONS:
        return {"allowed": False, "reason": "physical or consequential execution is outside reference-system scope"}

    missing = [key for key in REQUIRED_REVIEWS if not context.get(key)]
    if missing:
        return {"allowed": False, "reason": "missing required review", "missing": missing}

    blockers = []
    if context.get("unresolved_high_risk_hazard"):
        blockers.append("unresolved high-risk hazard")
    if context.get("unsafe_navigation"):
        blockers.append("navigation safety not demonstrated")
    if context.get("perception_uncertainty_high"):
        blockers.append("perception uncertainty too high")
    if context.get("unsafe_human_proximity"):
        blockers.append("human proximity risk unresolved")
    if context.get("emergency_stop_failed"):
        blockers.append("emergency-stop verification failed")
    if context.get("privacy_intrusion"):
        blockers.append("privacy risk unresolved")
    if context.get("cybersecurity_gap"):
        blockers.append("cybersecurity gap unresolved")

    if blockers:
        return {"allowed": False, "reason": "governance blocker", "blockers": blockers}

    return {"allowed": True, "reason": "analysis/review release approved by qualified human"}
