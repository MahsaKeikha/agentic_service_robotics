from orchestration.orchestrator import run

context = {
    "objective": "review a simulated indoor service robot deployment",
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

print(run(context))
