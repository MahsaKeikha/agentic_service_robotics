from AGENTS.deployment_readiness_agent import DeploymentReadinessAgent
from AGENTS.human_interaction_agent import HumanInteractionAgent
from AGENTS.mission_planner_agent import MissionPlannerAgent
from AGENTS.navigation_review_agent import NavigationReviewAgent
from AGENTS.perception_review_agent import PerceptionReviewAgent
from AGENTS.safety_agent import SafetyAgent
from safety.gate import authorize

AGENTS = [
    MissionPlannerAgent(),
    NavigationReviewAgent(),
    HumanInteractionAgent(),
    PerceptionReviewAgent(),
    SafetyAgent(),
    DeploymentReadinessAgent(),
]


def run(context: dict) -> dict:
    """Run all specialists and apply the fail-closed reference-release gate."""
    results = [agent.run(context) for agent in AGENTS]
    governance = authorize("analysis_release", context)
    return {
        "system": "F72",
        "results": results,
        "governance": governance,
        "release_allowed": governance["allowed"],
        "physical_actuation": False,
        "autonomous_deployment": False,
    }
