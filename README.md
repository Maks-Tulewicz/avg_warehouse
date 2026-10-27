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
│   │   ├── state.py           # System state representation
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
│       │   ├── package.xml
│       │   └── src/
│       │       └── supervisor_node.py
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
│   ├── literature.md         # Annotated bibliography
│   └── user_guide.md
├── scripts/
│   ├── run_simulation.py      # CLI for simulation experiments
│   ├── visualize_state.py     # ASCII/grid state viewer
│   └── reachability_check.py  # Reduced instance exhaustive analysis
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── requirements.txt           # Pure Python dependencies
├── requirements-dev.txt       # Dev tools
├── README.md                  # This file
└── CHANGELOG.md
```

---

## Quick Start

### Environment Setup

**Requirements**: Docker 20+, Docker Compose v2 (plugin), Linux/macOS or WSL2 with X-server (Windows)

```bash
# Clone and enter repository
git clone <repo-url> && cd avg_warehouse

# Build Docker image (once)
make build

# Start container in background
make up

# Enter the container
make shell
```

### Inside the Container

```bash
# Run simulation (pure Python, no ROS)
python3 scripts/run_simulation.py --robots 10 --orders 50 --duration 3600

# Run tests
python3 -m pytest tests/ -v

# Build ROS 2 packages
colcon build --symlink-install

# Visualize warehouse state
python3 scripts/visualize_state.py
```

### Exiting and Cleanup

```bash
# Exit container
exit

# Stop containers
make down

# Clean build artifacts
make clean
```

---

## Requirements Files

### `requirements.txt` (Pure Python)

```
numpy>=1.24,<2
networkx>=3.1
matplotlib>=3.7
```

**Important**: Does NOT contain any ROS 2 packages (rclpy, rosidl, *-msgs). Those are installed via apt in the Docker image.

### `requirements-dev.txt` (Dev Tools)

```
pytest>=7.3
pytest-cov>=4.1
flake8>=6.0
black>=23.7
isort>=5.12
```

---

### Troubleshooting Docker

**Problem**: `docker compose` command not found  
**Solution**: Install Docker Compose plugin:
```bash
sudo apt-get install docker-compose-plugin
docker compose version
```

**Problem**: GUI apps (Gazebo/RViz) won't start  
**Solution**: Ensure DISPLAY variable is set:
```bash
export DISPLAY=:0
docker compose up -d
```

On Windows (WSL2): Install VcXsrv or Xming, set `DISPLAY=$(hostname).local:0`.

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

### Commit Convention

```
type(scope): description

Examples:
- feat(model): add warehouse layout loader
- fix(supervisor): correct deadlock avoidance edge case
- chore(docker): update requirements, remove ROS packages
- docs: update README with new commands
```

---

## Testing

```bash
# All tests
python3 -m pytest tests/ -v

# Specific module
python3 -m pytest tests/test_safety.py -v

# With coverage
python3 -m pytest tests/ --cov=src --cov-report=html

# Linting
flake8 src/
black --check src/ tests/
```

---

## Milestones

| Milestone | Deadline | Deliverable |
|-----------|----------|-------------|
| **M1** | 20 Oct 2026 | Proposal report (problem, model concept, plan) |
| **M2** | 20 Nov 2026 | Formal model, safety proof, simulator KPIs, reachability analysis |
| **M3** | 11 Dec 2026 | 10-robot ROS 2/Gazebo demonstration |
| **M4** | 22 Dec 2026 | Final report, presentation, source archive |

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

## Key Performance Indicators

- **Throughput Θ**: Orders delivered per hour
- **Mean Lead Time**: Time from order arrival to delivery
- **Max Lead Time**: Worst-case order latency
- **Fleet Utilisation**: Percentage of time robots are active
- **Blocked Time**: Time spent waiting for cells

---
---

## Team Roles

| Member | Index | Responsibilities |
|--------|-------|------------------|
| Jakub Wilczyński | 275459 | Coordinator, formal model (T2), supervisor node (T7), experiments (T8) |
| Nylan Santos | 300482 | Formal model (T2), safety proof (T3), verification (T4) |
| Antoni Piałucha | 275411 | Simulator (T4), Gazebo world (T5), KPI evaluation (T8) |
| Maksymilian Tulewicz | 275421 | ROS 2 nodes (T6), integration (T7), demo video (T9) |

---

## Project Management

- **Weekly Standups**: Monday evenings, 30 minutes
- **Communication**: Discord server (24h response on working days)
- **Code Review**: Pull requests require 1 approval, passing CI
- **Documentation**: LaTeX reports via Overleaf, diagrams in TikZ


---
