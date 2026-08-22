from orchestration.orchestrator import run

REFERENCE_CONTEXT = {
    "objective": "service robotics engineering review",
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

if __name__ == "__main__":
    print(run(REFERENCE_CONTEXT))
