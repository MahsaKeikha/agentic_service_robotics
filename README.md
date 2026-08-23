# F72 Agentic Service Robotics

**Maturity:** L3 Gold Standard  
**Version:** 1.0.0

A governed six-agent reference architecture for service-robotics engineering across mission planning, navigation review, human-robot interaction, perception review, safety analysis, and deployment readiness.

F72 is designed for service robots operating in human environments such as offices, campuses, hospitality spaces, warehouses, hospitals, retail areas, research facilities, and other semi-structured environments. It supports engineering analysis, scenario review, hazard identification, deployment-readiness assessment, and human oversight. It is not a physical robot controller and does not authorize autonomous actuation.

## Why service robotics needs explicit governance

Service robots operate in environments that are less controlled than traditional industrial cells. They may encounter people, children, pets, wheelchairs, carts, doors, elevators, temporary obstacles, reflective surfaces, changing lighting, crowds, network outages, map drift, localization failures, and ambiguous social situations.

A useful reference lifecycle is:

```text
mission definition
      |
      v
navigation review
      |
      v
perception review
      |
      v
human interaction review
      |
      v
safety analysis
      |
      v
deployment readiness
      |
      v
qualified human approval
```

F72 separates these concerns so an apparently successful navigation plan cannot hide a perception, interaction, privacy, or safety blocker.

## Six-agent architecture

| Agent | Responsibility | Core question |
|---|---|---|
| Mission Planner Agent | Defines service objective, route context, task sequence and operational assumptions | Is the requested mission appropriate, bounded, and sufficiently specified for review? |
| Navigation Review Agent | Reviews maps, localization, path assumptions, obstacle handling and route feasibility | Can the robot navigate the environment safely under expected and degraded conditions? |
| Human Interaction Agent | Reviews communication, proximity, yielding, accessibility, social behavior and consent-related interaction concerns | Is the robot's behavior understandable, respectful, accessible, and safe around people? |
| Perception Review Agent | Reviews sensor coverage, object/person detection, uncertainty and environmental failure modes | Is the robot's environmental understanding sufficiently reliable for the intended task? |
| Safety Agent | Consolidates hazards, safety functions, emergency behavior and residual risks | Are hazards controlled and fail-safe behavior defined? |
| Deployment Readiness Agent | Reviews operational, cybersecurity, maintenance, monitoring and human-approval evidence | Is there enough verified evidence for a qualified human to consider deployment? |

No agent can independently authorize physical execution.

## Repository structure

```text
AGENTS/
├── mission_planner_agent.py
├── navigation_review_agent.py
├── human_interaction_agent.py
├── perception_review_agent.py
├── safety_agent.py
└── deployment_readiness_agent.py

SKILLS/
├── mission_design.py
├── navigation_review.py
├── human_robot_interaction.py
├── safety_case.py
└── deployment_readiness.py

TOOLS/
├── hazard_tool.py
├── map_audit_tool.py
├── scenario_tool.py
├── interaction_log_tool.py
└── readiness_tool.py

orchestration/
memory/
state/
schemas/
prompts/
config/
safety/
observability/
evals/
benchmarks/
examples/
tests/
docs/
.github/workflows/ci.yml
run.py
pyproject.toml
README.md
```

The architecture separates reasoning from deterministic evidence handling, safety gates, observability, state, and evaluation.

## Mission definition

The Mission Planner Agent starts by making the operational request explicit.

A mission record can include:

```text
mission_id
task_type
start_location
target_location
route_constraints
payload
operating_hours
human_contact_expected
restricted_zones
speed_limit
required_permissions
fallback_behavior
human_supervisor
```

Examples of service-robot missions can include delivery, inspection, guidance, transport support, inventory support, hospitality assistance, research tasks, and other non-safety-critical service functions.

Tasks involving medical treatment, emergency response, security enforcement, unrestricted physical handling of people, or other consequential authority require additional domain-specific controls.

## Mission boundaries

The mission should state what the robot is not allowed to do.

Typical prohibited or restricted behaviors can include:

- entering unauthorized spaces
- bypassing access controls
- using stairs unless specifically designed and validated
- pushing through crowds
- making physical contact with people without intended and validated interaction design
- operating outside approved hours or zones
- transporting prohibited or unsafe payloads
- continuing after a safety-critical sensor failure
- executing commands when localization is invalid

The mission model should fail closed when these boundaries are unclear.

## Navigation review

The Navigation Review Agent evaluates whether the planned mobility behavior is appropriate for the environment.

Relevant evidence includes:

- map source and version
- localization method
- route topology
- floor transitions
- obstacle policy
- speed limits
- stopping distance
- turning envelope
- doorway clearance
- corridor width
- ramp and slope limits
- floor-surface assumptions
- no-go zones
- recovery behavior

`TOOLS/map_audit_tool.py` supports deterministic review of map and navigation assumptions.

## Mapping and localization

A service robot should not assume that a previously valid map remains correct forever.

Potential sources of map or localization error include:

- furniture movement
- temporary construction
- closed corridors
- moved shelves
- reflective surfaces
- glass walls
- poor visual texture
- lighting changes
- wheel slip
- elevator transitions
- sensor occlusion
- map-version mismatch

Useful states include:

```text
MAP VALID
MAP STALE
LOCALIZATION DEGRADED
LOCALIZATION LOST
ROUTE BLOCKED
MANUAL REVIEW REQUIRED
```

A robot with uncertain localization should transition to a safe behavior rather than continue as if pose were known.

## Dynamic obstacle handling

Service robots frequently operate around moving obstacles.

The review should consider:

- pedestrians
- children
- mobility aids
- wheelchairs
- carts
- forklifts
- pets
- opening doors
- groups of people
- queues
- people stepping backward
- objects placed suddenly in the path

Navigation should preserve stopping margin and avoid relying on perfectly predictable human movement.

## Human proximity

Safety should consider distance, speed, visibility, approach direction, stopping capability, and context.

A robot moving slowly in an open corridor is not equivalent to the same robot approaching a seated person, a child, a patient, or someone using a mobility aid.

High-risk or poorly characterized proximity scenarios should block deployment-readiness claims until reviewed.

## Perception review

The Perception Review Agent evaluates the sensors and models the robot uses to understand its surroundings.

Potential sensor modalities include:

- lidar
- depth cameras
- RGB cameras
- stereo cameras
- ultrasonic sensors
- radar
- bump sensors
- wheel encoders
- IMU
- microphone arrays where applicable

The review should capture sensor placement, field of view, blind zones, range, update rate, environmental limitations, calibration, and failure behavior.

## Perception uncertainty

Perception output should not be treated as certain merely because the model returned a class label.

The system should reason about:

- confidence
- unknown-object states
- sensor disagreement
- partial occlusion
- low light
- glare
- glass
- reflective materials
- dense crowds
- motion blur
- environmental noise

High perception uncertainty should reduce robot authority and can trigger stop, slow-down, re-localization, or human review depending on the application.

## Sensor disagreement

Multi-sensor systems may disagree.

Examples include:

- camera sees a free path while lidar detects an obstacle
- map says a doorway exists but depth sensing indicates obstruction
- odometry suggests motion while localization remains stationary
- one sensor becomes stale while others continue updating

The architecture should define which signals are safety-related and how disagreement is handled.

## Human-robot interaction

The Human Interaction Agent reviews how the robot behaves around people.

Useful design dimensions include:

- approach distance
- yielding behavior
- right-of-way policy
- signaling intent
- audible and visual cues
- speech interaction
- accessibility
- understandable stop behavior
- polite recovery from blocking
- personal-space expectations
- interaction timeout
- human override

`TOOLS/interaction_log_tool.py` provides a reference record for reviewed interaction scenarios.

## Social navigation

Navigation in human environments is not only geometry.

A socially acceptable route may differ from the shortest path. The robot may need to avoid cutting through groups, blocking doors, stopping too close to people, or approaching from behind without signaling.

These behaviors should be tested in representative scenarios rather than inferred from map-level path planning alone.

## Accessibility

Service robotics should account for people with different physical, sensory, cognitive, and communication needs.

Relevant considerations can include:

- wheelchair clearance
- reduced walking speed
- hearing impairment
- visual impairment
- language differences
- inability to quickly move out of the robot's path
- assistive-device interaction

Accessibility should be considered part of safe deployment design, not an optional interface refinement.

## Privacy

Service robots can collect sensitive environmental and personal information simply by operating in human spaces.

Potentially sensitive data includes:

- images
- video
- audio
- faces
- voices
- location traces
- room occupancy
- behavior patterns
- access-control events
- interaction history

A privacy review should address:

- whether the data are necessary
- whether processing can occur locally
- retention
- recording indicators
- consent or notice where required
- access control
- secondary use
- model training
- deletion
- incident handling

A robot should not collect or retain data merely because a sensor makes it technically possible.

## Safety analysis

The Safety Agent consolidates hazards and controls.

`TOOLS/hazard_tool.py` provides the deterministic hazard-record abstraction.

A hazard record can include:

```text
hazard_id
scenario
hazard
initiating_condition
potential_harm
risk_level
control
verification
residual_risk
owner
status
```

Potential service-robot hazards include:

- collision with a person
- trapping or pinching
- falling payload
- runaway motion
- incorrect door transition
- localization loss
- blind-zone collision
- battery thermal event
- unstable charging behavior
- unsafe recovery maneuver
- cybersecurity compromise

## Emergency stop

Emergency-stop behavior is a hard safety boundary.

Deployment-readiness evidence should establish, as applicable:

- physical emergency-stop availability
- stop response time
- stop category or behavior
- restart conditions
- reset authority
- visibility and accessibility
- test evidence
- behavior after communication loss

F72 does not authorize bypassing, disabling, remotely defeating, or masking emergency-stop behavior.

## Safe states

The robot should define safe responses to degraded or uncertain conditions.

Examples include:

```text
STOP
SLOW MODE
HOLD POSITION
RETREAT TO SAFE LOCATION
REQUIRE HUMAN ASSISTANCE
DISABLE TASK EXECUTION
```

A safe state should be appropriate to the actual environment. Stopping in the middle of a fire exit or doorway may itself be unsafe, so deployment-specific review remains necessary.

## Doors and elevators

Doors and elevators introduce complex physical and operational dependencies.

A service robot may need to coordinate with:

- automatic doors
- access-control systems
- elevator controllers
- building-management systems
- door sensors
- human assistance

F72 does not autonomously authorize door unlocking, access-control changes, elevator commands, or building-control writes.

These integrations require independently governed permissions, interface validation, cybersecurity review, and fail-safe behavior.

## Charging and battery safety

Deployment planning should consider:

- battery state of charge
- charging location
- charger alignment
- thermal behavior
- damaged battery handling
- evacuation paths
- docking failures
- charger communication failure
- end-of-life battery policy

Battery constraints should feed mission planning so the robot does not begin a mission it cannot safely complete.

## Cybersecurity

Service robots are networked cyber-physical systems.

Security review should consider:

- device identity
- operator authentication
- authorization
- role separation
- least privilege
- secure communications
- software update integrity
- firmware integrity
- secrets management
- remote-access controls
- logging
- command integrity
- replay protection
- denial-of-service behavior
- third-party dependency risk

A compromised robot can create physical as well as privacy risk.

## Communications loss

The robot should have defined behavior when wireless or cloud connectivity fails.

Possible policies include:

- continue a locally validated low-risk action
- stop safely
- return to a defined location
- enter degraded mode
- require local human intervention

The correct behavior depends on the mission and safety analysis.

## Deployment readiness

The Deployment Readiness Agent consolidates evidence rather than simply checking whether the software starts.

`TOOLS/readiness_tool.py` provides the deterministic readiness abstraction.

Readiness review can include:

- approved mission envelope
- verified map
- localization performance
- dynamic obstacle tests
- perception review
- HRI review
- accessibility review
- hazard closure
- emergency-stop verification
- safe-state verification
- privacy review
- cybersecurity review
- charging review
- maintenance plan
- monitoring plan
- incident-response plan
- operator training
- human approval

## Scenario-based evaluation

`TOOLS/scenario_tool.py` supports scenario-driven analysis.

Representative cases should include:

- crowded corridor
- unexpected child movement
- wheelchair crossing path
- blocked doorway
- glass wall
- reflective floor
- localization loss
- sensor dropout
- communication outage
- failed elevator integration
- emergency-stop activation
- low-battery mission interruption

Scenario testing should include adverse and degraded conditions, not only nominal demonstrations.

## Maintenance and lifecycle

A service robot can become unsafe after deployment if hardware, sensors, software, maps, or environments change.

Lifecycle controls should consider:

- sensor calibration
- wheel and brake wear
- bumper inspection
- battery health
- camera/lidar cleanliness
- software version
- firmware version
- cybersecurity patches
- map updates
- incident trends
- near misses
- changed building layouts

Material changes should trigger reassessment rather than being assumed safe because a previous version passed review.

## Observability

The `observability/` layer supports traceable workflow execution and can be extended with fleet telemetry.

Useful service-robot metrics include:

- mission completion rate
- navigation abort rate
- localization-loss events
- obstacle-stop events
- perception-confidence distribution
- emergency-stop activations
- manual interventions
- near-miss reports
- battery-related aborts
- communication failures
- privacy incidents
- software version distribution

Operational metrics support monitoring but do not replace safety validation.

## Fail-closed governance

F72 blocks deployment-readiness claims when material evidence is missing or failed.

Release blockers include:

- mission undefined
- map invalid or stale
- localization not verified
- unsafe navigation
- dynamic obstacle handling unverified
- perception uncertainty high or unbounded
- unsafe human proximity
- HRI review incomplete
- accessibility review incomplete where relevant
- unresolved high-risk hazard
- emergency-stop verification failed or missing
- safe-state behavior unverified
- privacy review incomplete
- cybersecurity review incomplete
- door or elevator integration not independently authorized
- deployment monitoring incomplete
- incident-response readiness incomplete
- physical robot command requested
- direct actuator or controller write requested
- safety override requested
- autonomous deployment requested
- qualified human approval missing

Human approval is mandatory after automated gates pass. Human approval does not convert a failed safety control into a passing condition.

## Human authority boundaries

F72 must not autonomously:

- issue commands to physical robots
- actuate motors
- write to PLCs or building controllers
- unlock doors
- command elevators
- disable safety functions
- bypass emergency stops
- override human-access restrictions
- deploy a robot into a live environment
- approve a high-risk human-contact task
- suppress safety incidents

Physical execution remains with independently validated robot-control systems and authorized human operators.

## End-to-end reference workflow

A typical F72 review follows this sequence:

1. Define the service mission and prohibited behaviors.
2. Identify the environment, users, human-contact level, payload, and route constraints.
3. Audit map and localization assumptions.
4. Review navigation under nominal and degraded conditions.
5. Review perception coverage, uncertainty, blind zones, and sensor disagreement.
6. Review HRI, social navigation, accessibility, and privacy.
7. Build the hazard register.
8. Verify emergency-stop and safe-state evidence.
9. Review doors, elevators, charging, communications, and cybersecurity interfaces.
10. Run representative scenarios.
11. Review maintenance, observability, and incident-response readiness.
12. Consolidate unresolved risks.
13. Apply the fail-closed deployment-readiness gate.
14. Require explicit qualified human approval.

## Evaluation and held-out suite

The repository includes:

```text
evals/evaluate.py
evals/held_out.py
benchmarks/reference_case.json
```

The behavioral suite includes direct governance tests and a 10-scenario held-out safety evaluation.

Useful evaluation dimensions include:

- map validation
- localization-loss handling
- obstacle-response review
- perception-uncertainty enforcement
- human-proximity enforcement
- HRI review
- privacy enforcement
- cybersecurity enforcement
- emergency-stop enforcement
- door/elevator authority boundaries
- autonomous-actuation blocking
- deployment-readiness blocking
- human-approval enforcement

Strong held-out cases should intentionally contain unsafe or incomplete evidence.

## Failure states

Useful explicit states include:

```text
MISSION INCOMPLETE
MAP INVALID
LOCALIZATION UNVERIFIED
NAVIGATION UNSAFE
PERCEPTION UNCERTAINTY HIGH
HUMAN PROXIMITY UNSAFE
HRI REVIEW REQUIRED
PRIVACY REVIEW REQUIRED
CYBERSECURITY REVIEW REQUIRED
HIGH-RISK HAZARD OPEN
EMERGENCY STOP UNVERIFIED
SAFE STATE UNVERIFIED
DOOR/ELEVATOR AUTHORITY REQUIRED
DEPLOYMENT NOT READY
PHYSICAL EXECUTION PROHIBITED
HUMAN APPROVAL REQUIRED
```

The system should never fabricate map validity, localization quality, safety-function evidence, human approval, physical execution, or deployment authorization.

## Reproduce the reference implementation

Install development dependencies:

```bash
python -m pip install -e '.[dev]'
```

Run CI-equivalent checks:

```bash
ruff check . --select E9,F63,F7,F82
python -m pytest -q
python evals/held_out.py
python examples/example.py
python run.py
```

CI under `.github/workflows/ci.yml` validates Python 3.10, 3.11, and 3.12.

## L3 Gold Standard

F72 follows the library's L3 Gold Standard structure through specialist-agent separation, deterministic tools, explicit safety gates, held-out evaluation, observability, CI, state management, and mandatory human approval.

This maturity designation describes the engineering structure of the reference repository. It is not product certification, site approval, functional-safety certification, regulatory approval, or authorization to deploy a robot in a live environment.

## Extending F72

Common extensions include:

- ROS or ROS 2 research adapters
- mapping and localization systems
- fleet-management platforms
- indoor navigation stacks
- HRI interfaces
- accessibility interfaces
- elevator gateways
- automatic-door interfaces
- charging systems
- building-management integrations
- perception-quality dashboards
- telemetry and fleet observability
- maintenance systems
- incident reporting
- digital twins
- simulation environments

Extensions should preserve the separation between analysis, safety approval, physical-control authority, and real-world execution.

## Example applications

F72 can serve as a reference architecture for:

- indoor delivery robots
- hospitality robots
- campus service robots
- warehouse support robots
- hospital logistics robots
- retail service robots
- office robots
- inspection robots
- research mobile robots
- fleet-governance studies

Applications involving direct patient care, physical assistance, security enforcement, hazardous environments, or safety-critical operations require additional domain-specific controls.

## Design principles

1. Define mission boundaries before route planning.
2. Treat maps and localization as versioned safety evidence.
3. Design for dynamic human environments rather than static obstacles.
4. Make perception uncertainty visible and actionable.
5. Include social navigation, accessibility, and privacy in HRI review.
6. Treat emergency-stop and safe-state verification as hard gates.
7. Govern doors, elevators, chargers, and building interfaces independently.
8. Protect cyber-physical control paths with strong cybersecurity.
9. Fail closed when deployment evidence is incomplete.
10. Keep physical execution and deployment authority with qualified humans and validated control systems.

## Documentation

Additional architecture documentation is available under `docs/`, including `docs/ARCHITECTURE.md`.

## Citation and reuse

Use the repository metadata and citation information supplied by the project when referencing this implementation. The repository can be studied, cited, adapted, and extended subject to its license terms.

## Responsible use

Use F72 as a service-robotics engineering and multi-agent governance reference. Validate maps, localization, perception, HRI, privacy, cybersecurity, emergency-stop behavior, safe states, integrations, maintenance, monitoring, and site-specific hazards against the actual robot and deployment environment. Final physical execution and deployment decisions remain with appropriately qualified and authorized humans.