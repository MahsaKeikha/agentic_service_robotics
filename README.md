# F72 | Agentic Service Robotics | L3 Gold Standard | v1.0

A governed multi-agent reference implementation for service robotics mission planning, navigation review, perception review, human-robot interaction, safety analysis, and deployment readiness.

## Six-agent architecture

- [Mission Planner](AGENTS/mission_planner_agent.py)
- [Navigation Review](AGENTS/navigation_review_agent.py)
- [Human Interaction](AGENTS/human_interaction_agent.py)
- [Perception Review](AGENTS/perception_review_agent.py)
- [Safety](AGENTS/safety_agent.py)
- [Deployment Readiness](AGENTS/deployment_readiness_agent.py)

Tools and skills are exposed in `TOOLS/` and `SKILLS/`. Supporting layers include orchestration, memory, state, schemas, prompts, config, safety, observability, evals, benchmarks, examples, tests, docs, and CI.

## Gold-standard governance

F72 is fail closed. Analysis release requires mission, navigation, perception, human-interaction, hazard, emergency-stop, privacy, cybersecurity, and deployment-readiness review plus explicit qualified human approval.

Release is blocked for unresolved high-risk hazards, unsafe navigation, high perception uncertainty, unsafe human proximity, failed emergency-stop verification, privacy intrusion, or cybersecurity gaps.

Physical or consequential execution is outside this reference system's authority. Robot commands, actuation, safety overrides, autonomous deployment, and autonomous door/elevator control are never authorized by the agentic system.

## Verification gates

CI runs on Python 3.10, 3.11, and 3.12 and requires:

```bash
ruff check . --select E9,F63,F7,F82
python -m pytest -q
python evals/held_out.py
python examples/example.py
python run.py
```

The behavioral suite includes direct governance tests and a 10-scenario held-out safety evaluation.
