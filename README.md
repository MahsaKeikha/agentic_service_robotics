# F72 Agentic Service Robotics

Standalone multi-agent reference implementation for service robotics planning, human interaction design, navigation review, safety analysis, and deployment readiness.

Agents: [Mission Planner](AGENTS/mission_planner_agent.py), [Navigation Review](AGENTS/navigation_review_agent.py), [Human Interaction](AGENTS/human_interaction_agent.py), [Perception Review](AGENTS/perception_review_agent.py), [Safety](AGENTS/safety_agent.py), [Deployment Readiness](AGENTS/deployment_readiness_agent.py).

Tools and skills are exposed in `TOOLS/` and `SKILLS/`. Supporting layers include orchestration, memory, state, schemas, prompts, config, safety, observability, evals, benchmarks, examples, tests, docs, and CI.

Physical actuation is outside scope. Any deployment requires qualified human authorization.
