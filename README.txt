# Deadlock-Free Event-Based Control of Mobile Robot Fleet

**Course**: Event-Based Control, Wrocław University of Science and Technology  
**Project ID**: avg_warehouse  
**Team**: Jakub Wilczyński, Nylan Santos, Antoni Piałucha, Maksymilian Tulewicz  
**Instructor**: Gurjinder Singh  
**Timeline**: October 2026 - December 2026 (10 weeks)

---

## Overview

This project implements a supervisory, event-based control system for a fleet of 10 autonomous mobile robots (AGVs) operating in an automated grid warehouse. The core challenge is **deadlock-free coordination** using discrete-event system (DES) formalism with resource-allocation safety guarantees.

### Key Components

1. **Formal Model**: Finite-state automaton representing warehouse layout, robot states, and events
2. **Safety Supervisor**: Real-time deadlock avoidance using Banker's algorithm variant
3. **Event Prioritisation**: Rules for cell conflicts, intersections, order assignment, charging
4. **Discrete-Event Simulator**: Python-based simulation with KPI logging
5. **ROS 2 Integration**: Real-world demonstration with Gazebo simulation

---

## Repository Structure

```
avg_warehouse/
├── .github/
│   └── workflows/
│       ├── test.yml           # GitHub Actions for pytest
│       └── lint.yml           # PEP 8 / flake8 checks
├── src/
│   ├── model/
│   │   ├── __init__.py
│   │   ├── warehouse.py       # Grid layout, graph G=(V,A)
│   │   ├── robot.py           # Robot state tuple si
│   │   ├── events.py          # Event definitions, EF(s)
│   │   └── transitions.py     # next_state(s, e) function
│   ├── supervisor/
│   │   ├── __init__.py
│   │   ├── safety.py          # safe(s, e) algorithm
│   │   ├── priorities.py      # R1-R5 prioritisation rules
│   │   └── dispatcher.py      # Order assignment logic
│   ├── simulator/
│   │   ├── __init__.py
│   │   ├── engine.py          # Discrete-event simulation loop
│   │   ├── generators.py      # Random order streams
│   │   └── kpi.py             # Throughput, lead time metrics
│   └── ros2/
│       ├── fleet_supervisor/  # ROS 2 node package
│       │   ├── CMakeLists.txt
│   │       ├── package.xml
│       │   └── src/
│       │       └── supervisor_node.cpp
│       └── robot_nodes/
│           └── robot_controller/
├── tests/
│   ├── __init__.py
│   ├── test_model.py
│   ├── test_safety.py
│   ├── test_priorities.py
│   └── test_reachability.py   # Exhaustive BFS for reduced instance
├── data/
│   ├── layouts/
│   │   └── warehouse_15x8.json # Grid configuration
│   ├── orders/
│   │   └── sample_batch.json  # Test order sequences
│   └── logs/
│       └── runs/              # Simulation logs per experiment
├── notebooks/
│   └── analysis.ipynb         # KPI visualisation, policy comparison
├── docs/
│   ├── proposal.pdf          # Milestone 1
│   ├── interim_report.pdf    # Milestone 2
│   ├── final_report.pdf      # Milestone 4
│   └── user_guide.md
├── scripts/
│   ├── run_simulation.py      # CLI for simulation experiments
│   ├── visualize_state.py     # ASCII/grid state viewer
│   └── reachability_check.py  # Reduced instance exhaustive analysis
├── .gitignore
├── .flake8
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── README.md                  # This file
└── CHANGELOG.md
```

---

## Quick Start

### Environment Setup

```bash
# Clone and enter repository
git clone <repo-url> && cd avg_warehouse

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run basic simulation
python scripts/run_simulation.py --robots 10 --orders 50 --duration 3600
```

### Requirements Export

After activating venv and installing packages:
```bash
pip freeze > requirements.txt
pip freeze > requirements-dev.txt  # dev packages separately
```

---

## Core Concepts

### State Representation

System state: `s = (s₁, s₂, ..., s₁₀, Q, n)`

Where each robot state `sᵢ = (Hᵢ, mᵢ, bᵢ, oᵢ, gᵢ)`:
- `Hᵢ`: Sequence of cells held by robot (position + reserved cells)
- `mᵢ`: Operating mode (Idle, ToPick, Loaded, ToDrop, ToCharge, etc.)
- `bᵢ`: Battery level (moves remaining)
- `oᵢ`: Assigned order (or ⊥ if none)
- `gᵢ`: Reserved goal buffer cell (or ⊥ if none)

### Events

| Type | Name | Controllable | Description |
|------|------|--------------|-------------|
| UC | `order(o)` | No | New order arrives from WMS |
| C | `assign(i, o)` | Yes | Assign order to robot |
| C | `dispatch(i, g)` | Yes | Reserve goal buffer cell |
| C | `enter(i, v)` | Yes | Allow robot to enter cell |
| UC | `arrive(i)` | No | Robot completed move |
| UC | `loaded(i)` | No | Loading/unloading finished |

### Safety Guarantee

Algorithm `safe(s, e)` ensures deadlock freedom by verifying that after any proposed event, there exists a completion order where all robots can reach their reserved goals without circular wait.

---

## Milestones

| Milestone | Deadline | Deliverable |
|-----------|----------|-------------|
| M1 | 20 Oct 2026 | Proposal report (this doc) |
| M2 | 20 Nov 2026 | Formal model, safety proof, simulator KPIs |
| M3 | 11 Dec 2026 | 10-robot ROS 2/Gazebo demo |
| M4 | 22 Dec 2026 | Final report, presentation, source archive |

---

## Development Workflow

### Branch Strategy

```
main                          # Production-ready code
├── develop                   # Integration branch
│   ├── feature/model-core
│   ├── feature/safety-algo
│   ├── feature/simulator
│   └── feature/ros2-integration
└── hotfix/*                  # Urgent bug fixes
```

### Pull Request Process

1. Create feature branch from `develop`
2. Implement changes with tests
3. Submit PR for review (minimum 1 approver)
4. CI must pass (pytest + flake8)
5. Merge to `develop`
6. Tag releases at milestones: `m1`, `m2`, `m3`, `v1.0`

---

## Key Performance Indicators

- **Throughput Θ**: Orders delivered per hour
- **Mean Lead Time**: Time from order arrival to delivery
- **Max Lead Time**: Worst-case order latency
- **Fleet Utilisation**: Percentage of time robots are active
- **Blocked Time**: Time spent waiting for cells

---

## Testing

```bash
# All tests
pytest tests/ -v

# Specific module
pytest tests/test_safety.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Reachability analysis (reduced instance)
python scripts/reachability_check.py --robots 4 --layout small
```

---

## References

See `docs/literature.md` for annotated bibliography on RAS, AGV deadlock avoidance, and discrete-event control.

---

## License

Private during semester. May be published under MIT license after grading with team consent.

---

## Contact

- **Coordinator**: Jakub Wilczyński (275459)
- **Instructor**: Gurjinder Singh
- **Communication**: Team Discord 
- **Issue Tracking**: GitHub Projects board