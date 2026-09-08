# jfxjts

## OpenTwin Flight --- Open Flight Training & Mission Simulation Platform

> Open-source reference architecture and technology compendium for
> AI-assisted pilot training, mission rehearsal, distributed simulation,
> Modelica-based multidomain engineering, modular aircraft digital
> twins, and interoperable training environments.

**jfxjts** consolidates an open engineering architecture for flight
training and mission simulation using **MBSE, flight dynamics,
Modelica/FMI, HLA/distributed simulation, ROS 2/DDS, AI, digital twins,
synthetic environments, and modular mission interfaces**.

## Vision

**MBSE + Flight Simulation + Modelica/FMI + Distributed Simulation +
Digital Twins + AI**

The platform emphasizes open architecture, replaceable simulation
engines, multi-fidelity aircraft models, reproducible scenarios,
human-in-the-loop experimentation, AI-assisted instruction, and
technology independence.

## Objectives

-   Integrate MBSE with executable flight and mission models.
-   Define modular OpenTwin Flight interfaces.
-   Support replaceable flight-dynamics engines.
-   Support Modelica and FMI/FMU for multidomain subsystems.
-   Support HLA and message-oriented distributed simulation.
-   Connect telemetry to digital twins.
-   Support AI-assisted training, evaluation, and diagnostics.
-   Enable reusable mission scenarios and multi-vehicle simulation.
-   Separate core architecture, optional integrations, and research
    references.

## Reference Architecture

``` text
                    MISSION PROFILES
                         |
     +-----------+-------+---------+-----------+
     |           |                 |           |
  Training   Air Medical          SAR      Research
                         |
                         v
                  AI & AUTONOMY
                         |
                         v
                  OPENTWIN FLIGHT
                         |
              DIGITAL TWIN INTERFACE BUS
                         |
   +----------+----------+----------+----------+
   |          |          |          |          |
 Flight    Modelica     HLA       ROS 2      FMI
Dynamics               /RTI       /DDS       /FMU
   +----------+----------+----------+----------+
                         |
                SIMULATION SERVICES
                         |
       Aircraft | Environment | Mission
                         |
                  MBSE / MOSA / OMS
```

## OpenTwin Flight

OpenTwin Flight is a technology-neutral digital-twin layer capable of
representing a virtual aircraft, connected simulator, experimental
aircraft twin, mission-training environment, or distributed simulation
federation.

``` text
Aircraft / Simulator / Synthetic Asset
                  |
        Telemetry & Input Adapters
                  |
           Semantic Data Layer
                  |
        OpenTwin Flight Interface Bus
        |          |           |
 Flight Model   Avionics    Environment
        +----------+-----------+
                   |
             Twin State
                   |
      Training | Monitoring | Analytics
                   |
            Instructor / AI
```

## Modular Digital Twin Interfaces

### Aircraft Interface

Identity, configuration, mass properties, geometry reference,
flight-dynamics adapter, propulsion adapter, avionics adapter, and
health state.

### Flight Dynamics Interface

``` text
initialize()
configure_aircraft()
set_environment()
set_controls()
step(dt)
get_kinematics()
get_dynamics()
get_state()
reset()
shutdown()
```

### Propulsion Interface

Supports conventional, electric, hybrid-electric, battery,
hydrogen-oriented conceptual, and distributed-propulsion research
models.

### Avionics Interface

Flight instruments, navigation, communications, autopilot, flight
management, synthetic avionics, and instructor-injected failures.

### Sensor Interface

GNSS, IMU, air data, radar altimeter, weather radar, cameras, LiDAR,
AIS/ADS-B, and synthetic sensors.

### Environment Interface

Atmosphere, wind, turbulence, weather, terrain, water surface,
visibility, and time/lighting.

### Mission Interface

Objectives, routes, waypoints, events, constraints, success/failure
criteria, and evaluation metrics.

### Telemetry Interface

``` text
aircraft.position.*
aircraft.altitude
aircraft.attitude.*
aircraft.velocity.*
propulsion.power
energy.soc
controls.*
mission.phase
training.score
health.index
```

### Pilot / Operator Interface

Cockpit controls, HOTAS, low-cost controllers, instructor stations,
remote operator stations, and experimental autonomous-agent interfaces.

### AI Agent Interface

AI modules can consume observations and produce recommendations,
instructor cues, scenario adaptation, or simulated actions.
Safety-critical real-world control is outside this training
architecture.

### FMI / FMU Interface

Portable subsystem models for propulsion, electrical systems, batteries,
thermal management, hydraulics, actuators, environmental control, and
control logic.

### HLA / Distributed Simulation Interface

``` text
Federation
├── Aircraft Federate
├── Environment Federate
├── Mission Federate
├── Instructor Federate
├── Sensor Federate
├── AI Federate
├── Recorder Federate
└── Visualization Federate
```

### Health Interface

Aircraft, propulsion, avionics, sensor, simulation, and network health
plus confidence and recommended training action.

### Scenario Interface

Versioned scenario packages define aircraft, environment, mission,
failures, events, and scoring profiles.

### Visualization Interface

3D simulators, instructor dashboards, GIS/map clients, Grafana, Jupyter,
and experimental AR/VR clients.

### Model Registry

Tracks model ID, version, fidelity, provenance, compatibility,
validation status, and license.

## Digital Twin Profiles

``` text
Minimal Flight Simulation Twin
              |
Connected Aircraft Twin
              |
Mission Training Twin
              |
AI-Assisted Training Twin
              |
Distributed Multi-Vehicle Twin
```

The progression moves from aircraft/environment simulation to telemetry
and health, mission/instructor/scoring services, AI-assisted assessment,
and finally distributed multi-aircraft training.

## Training and Mission Profiles

-   **General Flight Training:** procedures, navigation, weather,
    abnormal events, recurrent and instrument-oriented simulation
    research.
-   **Air Medical:** time-critical mission rehearsal, route planning,
    landing-zone scenarios, and crew workflow simulation.
-   **Search & Rescue:** search patterns, maritime/terrain scenarios,
    sensors, coordination, and rescue-support decisions.
-   **Humanitarian & Logistics:** remote connectivity, cargo, disaster
    response, constrained infrastructure, and multi-aircraft
    coordination.
-   **Research & Autonomy:** AI agents, optionally piloted concepts,
    human-machine teaming, and synthetic sensor evaluation.

## Distributed Simulation

``` text
                   SCENARIO MANAGER
                         |
      +------------------+------------------+
      |                  |                  |
 Aircraft A          Aircraft B        Environment
      +------------------+------------------+
                         |
                DISTRIBUTED BUS / HLA
                         |
      Instructor | AI | Recorder | Visualization
```

Time synchronization, ownership, coordinate systems, units, and data
semantics must be explicitly documented.

## Modelica and FMI

Modelica can represent propulsion, electrical power, batteries, thermal
systems, hydraulics, actuation, environmental control, and control
systems. FMI/FMU provides a portable model-exchange boundary where
appropriate.

## AI-Assisted Training

Potential uses include maneuver classification, performance assessment,
anomaly detection, adaptive difficulty, instructor assistance,
trajectory analysis, debriefing, and synthetic traffic generation.

``` text
Telemetry + Scenario + Mission Context
                  |
             AI Analytics
       +----------+----------+
     Scoring   Feedback   Adaptation
       +----------+----------+
                  |
              Debriefing
```

AI scoring should be explainable and auditable, and qualified human
instructors remain authoritative where training decisions have real
consequences.

## Open-Source Technology Compendium

Technologies below are candidate integrations or research references
unless a module explicitly declares them required.

  -------------------------------------------------------------------------
  Domain                  Candidate technology /  Role
                          standard                
  ----------------------- ----------------------- -------------------------
  Flight simulation       FlightGear              Open flight simulation

  Flight dynamics         JSBSim-oriented         Flight-dynamics research
                          workflows               

  Multidomain modeling    Modelica / OpenModelica Physical-system modeling

  Model exchange          FMI / FMU               Portable simulation
                                                  components

  Distributed simulation  HLA / RTI ecosystem     Federation
                                                  interoperability

  Robotics messaging      ROS 2 / DDS             Modular messaging

  Autonomy simulation     AirSim-style workflows  Autonomous-system
                                                  research

  Air traffic research    BlueSky                 Air-traffic simulation

  Simulation framework    OpenEaagles             Architecture research

  Autopilot research      PX4 / ArduPilot         Optional autonomy
                                                  integration

  Robotics simulation     Gazebo                  Sensor/robotics
                                                  simulation

  Marine integration      MOOS-IvP                Optional maritime
                                                  research

  CFD                     OpenFOAM                Aerodynamic/environment
                                                  research

  AI / analytics          Python ecosystem        Analytics and ML

  Visualization           Blender / Grafana /     Visualization and
                          Jupyter                 analysis

  Containers              Docker                  Reproducible services

  Orchestration           Kubernetes              Distributed deployment
                                                  research
  -------------------------------------------------------------------------

## MBSE Engineering Process

``` text
Requirements
     |
Operational Analysis
     |
Mission Architecture
     |
Logical Architecture
     |
Physical Architecture
     |
 +---+-------------------+
 |                       |
CAD / Cockpit        CAS / Simulation
 |                       |
 +-----------+-----------+
             |
       OpenTwin Flight
             |
 Training / Mission Validation
```

Interfaces should be defined before implementation technologies are
selected.

## Recommended Repository Structure

``` text
jfxjts/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── MBSE/
├── aircraft/
├── simulation/
│   ├── flight-dynamics/
│   ├── environment/
│   ├── avionics/
│   └── scenarios/
├── modelica/
├── digital-twin/
│   ├── core/
│   ├── state/
│   ├── health/
│   └── registry/
├── interfaces/
│   ├── aircraft/
│   ├── flight-dynamics/
│   ├── propulsion/
│   ├── avionics/
│   ├── sensors/
│   ├── environment/
│   ├── mission/
│   ├── telemetry/
│   ├── operator/
│   ├── fmi/
│   ├── hla/
│   └── ros2/
├── training/
├── ai/
├── schemas/
└── docs/
```

## User Guide

1.  Define the training or mission objective.
2.  Capture requirements with MBSE.
3.  Select aircraft model and fidelity.
4.  Configure flight dynamics and subsystems.
5.  Configure environment and mission scenario.
6.  Configure pilot/operator and instructor interfaces.
7.  Enable optional distributed simulation.
8.  Execute the scenario and record telemetry/events.
9.  Synchronize OpenTwin Flight state.
10. Apply scoring and optional AI analytics.
11. Conduct debriefing.
12. Record model, scenario, and validation versions.

## Installation Guide

jfxjts is a reference architecture and compendium rather than a
mandatory monolithic distribution.

``` bash
git clone https://github.com/robotics-intelligent-systems/jfxjts.git
cd jfxjts
```

Conceptual research environment:

``` text
MBSE                -> Capella / Arcadia
Flight Simulation   -> FlightGear
Physical Modeling   -> OpenModelica
Model Exchange      -> FMI / FMU
Distributed Sim     -> HLA-compatible RTI
Messaging           -> ROS 2 / DDS
Autonomy            -> PX4 / ArduPilot
AI / Analysis       -> Python
Visualization       -> Grafana / Jupyter / Blender
Containers          -> Docker
```

Install only the components required for a specific experiment.
Executable modules should document exact tested versions, OS
requirements, SDKs, compilers, package managers, build procedures,
configuration, and tests.

## Dependencies

Three categories are maintained:

1.  **Required Dependencies** --- strictly required by an executable
    module.
2.  **Optional Integrations** --- replaceable engines, middleware,
    visualization, AI, autopilot, and model-exchange technologies.
3.  **Research References** --- technologies evaluated for comparison
    but not required to execute jfxjts.

Each integration should document version, purpose, interface, license,
required/optional status, and validation status.

## Roadmap

### Phase 1 --- Documentation and Architecture

-   [x] Consolidate project description.
-   [x] Apply BID-inspired README structure.
-   [x] Define OpenTwin Flight.
-   [x] Define modular digital-twin interfaces.
-   [ ] Normalize dependency/license metadata.

### Phase 2 --- Minimal Flight Twin

-   [ ] Canonical aircraft schema.
-   [ ] Flight-dynamics adapter.
-   [ ] Environment interface.
-   [ ] Twin-state API.
-   [ ] Telemetry recorder.

### Phase 3 --- Mission Training Twin

-   [ ] Scenario schema.
-   [ ] Mission interface.
-   [ ] Instructor API.
-   [ ] Scoring interface.
-   [ ] Debriefing pipeline.

### Phase 4 --- Modelica / FMI

-   [ ] Generic propulsion model.
-   [ ] Electrical/energy model.
-   [ ] Thermal model.
-   [ ] FMU integration.
-   [ ] Replaceable subsystem demonstration.

### Phase 5 --- Distributed Simulation

-   [ ] HLA adapter.
-   [ ] Time synchronization.
-   [ ] Shared environment.
-   [ ] Multi-aircraft scenario.
-   [ ] Recorder/replay service.

### Phase 6 --- AI-Assisted Training

-   [ ] Maneuver analytics.
-   [ ] Explainable scoring.
-   [ ] Adaptive scenarios.
-   [ ] Instructor-assistance prototype.
-   [ ] Automated debriefing experiment.

### Phase 7 --- Specialized Missions

-   [ ] Air-medical profile.
-   [ ] Search-and-rescue profile.
-   [ ] Humanitarian/logistics profile.
-   [ ] Maritime/island-connectivity profile.
-   [ ] Research/autonomy profile.

## How to Contribute

Contributions are welcome in flight simulation, Modelica/FMI, avionics,
HLA/distributed simulation, ROS 2/DDS, AI training analytics, instructor
interfaces, mission scenarios, MBSE, visualization, validation, and
documentation.

``` bash
git checkout -b feature/my-contribution
git add .
git commit -m "Add: description of contribution"
git push origin feature/my-contribution
```

Pull requests should describe the problem, proposed solution, affected
interfaces, dependencies, licenses, validation method, and
test/simulation results.

## Code of Conduct

Contributors are expected to maintain a professional, inclusive, and
collaborative environment. A dedicated `CODE_OF_CONDUCT.md` should be
maintained in the repository root.

## Authors and Maintainers

Maintained by the **Robotics Intelligent Systems** open-source
initiative.

Project repository: `robotics-intelligent-systems/jfxjts`

Third-party projects retain their respective authorship, trademarks, and
licenses.

## Intellectual Property

jfxjts is intended to create original, sufficiently abstract, reusable
engineering and simulation interfaces. Third-party aircraft imagery,
simulator screenshots, technical references, and conceptual designs
should be treated as inspiration or comparative references unless
explicit reuse rights are available.

Avoid reproducing proprietary aircraft models, copyrighted engineering
drawings, restricted mission data, confidential specifications,
classified information, patented implementation details, or proprietary
training courseware.

## Disclaimer

jfxjts is a **research, educational, and experimental project**. It is
not an authority-approved flight-training device, certified flight
simulator, aviation training organization, avionics system,
flight-control system, operational planning system, or certification
tool.

Simulation and AI outputs must not be the sole basis for operating
aircraft, certifying pilots, making safety-critical aviation decisions,
or conducting real emergency operations.

Real-world applications require validated models, qualified professional
review, certified equipment where applicable, and compliance with
relevant aviation regulations and procedures.

The BID repository template is used solely as a documentation-structure
reference. jfxjts does not claim BID funding, endorsement, catalog
membership, or institutional affiliation.

## License

The applicable jfxjts project license should remain in the repository
root as `LICENSE`.

Third-party software, models, datasets, standards, and documentation
retain their respective licenses. Do not automatically apply the BID
software license merely because the BID documentation template was used
as a structural reference.

## Open Engineering Principles

**Open Standards · Modular Interfaces · Modelica/FMI · Distributed
Simulation · Digital Twins · AI-Assisted Training · Multi-Fidelity
Models**

> Define interfaces before implementations.\
> Model before integration.\
> Simulate before operation.\
> Validate before deployment.\
> Keep every simulation component replaceable.
