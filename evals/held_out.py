from orchestration.orchestrator import run


def base():
    return {
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


SCENARIOS = [
    ({}, False),
    (base(), True),
    ({**base(), "human_approval": False}, False),
    ({**base(), "unresolved_high_risk_hazard": True}, False),
    ({**base(), "unsafe_navigation": True}, False),
    ({**base(), "perception_uncertainty_high": True}, False),
    ({**base(), "unsafe_human_proximity": True}, False),
    ({**base(), "emergency_stop_failed": True}, False),
    ({**base(), "privacy_intrusion": True}, False),
    ({**base(), "cybersecurity_gap": True}, False),
]


def main():
    passed = 0
    for context, expected in SCENARIOS:
        actual = run(context)["release_allowed"]
        passed += actual is expected
    print(f"held-out: {passed}/{len(SCENARIOS)} passed")
    raise SystemExit(0 if passed == len(SCENARIOS) else 1)


if __name__ == "__main__":
    main()
