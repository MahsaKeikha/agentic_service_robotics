from AGENTS.mission_planner_agent import MissionPlannerAgent
from AGENTS.navigation_review_agent import NavigationReviewAgent
from AGENTS.human_interaction_agent import HumanInteractionAgent
from AGENTS.perception_review_agent import PerceptionReviewAgent
from AGENTS.safety_agent import SafetyAgent
from AGENTS.deployment_readiness_agent import DeploymentReadinessAgent
A=[MissionPlannerAgent(),NavigationReviewAgent(),HumanInteractionAgent(),PerceptionReviewAgent(),SafetyAgent(),DeploymentReadinessAgent()]
def run(c): return {"system":"F72","results":[a.run(c) for a in A],"physical_actuation":False}
