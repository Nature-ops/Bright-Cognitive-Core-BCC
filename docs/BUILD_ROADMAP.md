# Bright Assistant — Build Roadmap

## Mission

Bright Assistant is an AI-powered Engineering Operating System designed to help engineers:

- learn
- build
- automate
- practice
- assess
- document
- troubleshoot
- improve

The long-term objective is to evolve Bright from a structured engineering learning platform into an intelligent engineering operating system capable of understanding engineering projects and executing controlled engineering workflows.

---

# Current Status

Bright currently has two major application surfaces.

## Learning Platform

The learning platform supports:

- structured frameworks
- milestones
- skills
- resources
- exercises
- assessments
- objective progression
- exercise progression
- assessment scoring
- persistent progress
- resumable study sessions
- dependency-aware milestone planning
- automatic milestone progression
- CLI progress display

## AI Assistant

The FastAPI application provides the foundation for:

- chat
- AI provider abstraction
- prompts
- conversation memory
- health/API functionality

The learning platform and AI assistant are currently separate architectural surfaces and should not be unnecessarily coupled.

---

# Guiding Architecture

The intended high-level architecture is:

    Knowledge
        ↓
    Domain Models
        ↓
    Engines / Services
        ↓
    Planning
        ↓
    Study Sessions
        ↓
    Progress
        ↓
    Agent Capabilities
        ↓
    Engineering Automation

The eventual agent architecture is:

    User
      ↓
    Agent Planner
      ↓
    Task Manager
      ↓
    Tool Engine
      ↓
    Command Runner
      ↓
    Output Processor
      ↓
    Context Builder
      ↓
    AI Provider
      ↓
    Memory / Knowledge
      ↓
    Review / Safety Gate

---

# PHASE 0 — Foundation

Status: COMPLETE

## Completed

- [x] Repository established
- [x] Python application structure
- [x] FastAPI foundation
- [x] AI provider abstraction
- [x] Prompt service
- [x] Conversation memory
- [x] Learning domain models
- [x] YAML knowledge architecture
- [x] Knowledge loading
- [x] Learning framework loading
- [x] Planning engine
- [x] Resource engine
- [x] Exercise engine
- [x] Assessment engine
- [x] Study session service
- [x] Study engine
- [x] JSON framework progress
- [x] JSON study progress
- [x] CLI learning workflow

---

# PHASE 1 — Learning Workflow

Status: COMPLETE

## Completed

- [x] Framework milestone ordering
- [x] Milestone dependency handling
- [x] Objective progression
- [x] Exercise progression
- [x] Assessment scoring
- [x] Assessment answer normalization
- [x] CLI numbered assessment answers
- [x] CLI assessment result display
- [x] Framework progress display
- [x] Milestone completion
- [x] Resumable study sessions
- [x] Automatic milestone progression
- [x] Final framework completion
- [x] CLI integration test for milestone progression
- [x] Controller API for completed milestones

---

# PHASE 2 — Test Architecture

Status: IN PROGRESS

Goal:

Make Bright's tests deterministic, isolated, and independent from real learner state.

## Tasks

- [x] Isolate study-session tests from persistent progress
- [x] Add CLI milestone progression integration test
- [x] Verify assessment behavior
- [x] Verify milestone completion
- [ ] Convert important script-style tests into discoverable automated tests
- [ ] Standardize temporary persistence fixtures
- [ ] Remove accidental dependence on repository data
- [ ] Establish a consistent test helper layer
- [ ] Add regression coverage for framework completion
- [ ] Add regression coverage for dependency ordering
- [ ] Add regression coverage for session resumption

## Completion criteria

Tests must be runnable repeatedly without changing:

    data/progress.json

or other real learner state.

---

# PHASE 3 — Application Boundary Cleanup

Status: COMPLETE

Goal:

Keep UI, orchestration, domain logic, and persistence properly separated.

## Completed

- [x] CLI no longer directly accesses framework ProgressService
- [x] SessionController exposes completed milestone information
- [x] Automatic progression is controlled by SessionController
- [x] Audit CLI access to StudyEngine internals
- [x] Ensure CLI communicates through SessionController APIs
- [x] Remove active framework-progress and study-progress service leaks
- [x] Add focused controller APIs for framework progress rendering
- [x] Keep persistence implementations behind injected repository boundaries

## Deferred non-blockers

- Further encapsulate SessionController's existing session/objective read
  delegation only when a concrete caller requires a new application operation.
- Rename legacy internal service attribute names only as part of a focused
  migration that needs them.

## Rule

Do not introduce abstractions merely for abstraction's sake.

Create a boundary when it protects the architecture from implementation details.

---

# PHASE 4 — Persistence Architecture

Status: PLANNED

Goal:

Create a unified persistence boundary without changing application behavior.

Current architecture:

    PlanningEngine
        ↓
    ProgressService
        ↓
    progress.json

    StudyEngine
        ↓
    StudyProgressService
        ↓
    study_progress/*.json

Long-term architecture:

    Application / Domain
            ↓
    Repository Interfaces
            ↓
    Persistence Implementations
            ↓
    JSON / SQLite / PostgreSQL

## Planned sequence

### 4.1 Framework progress boundary

- [ ] Define domain-facing framework progress repository
- [ ] Preserve existing Progress behavior
- [ ] Introduce JSON implementation
- [ ] Keep JSON format unchanged
- [ ] Add isolated repository tests
- [ ] Update PlanningEngine dependency
- [ ] Update StudyEngine dependency

### 4.2 Study session progress boundary

- [ ] Define study-progress repository
- [ ] Preserve resumable sessions
- [ ] Add isolated tests
- [ ] Inject persistence dependency into StudyEngine

### 4.3 Exercise history

First decide whether ExerciseProgressService represents:

- obsolete duplicate persistence
- exercise history
- exercise attempts
- learner notes
- another future domain concept

Do not delete it until that decision is made.

### 4.4 Unified completion semantics

Current completion touches multiple persistence stores.

Future goal:

    Complete Milestone
          ↓
    Atomic persistence operation
          ↓
    Framework progress updated
          +
    Session state finalized

Avoid partial completion states.

### 4.5 Database implementation

Only after repository contracts are stable:

- [ ] SQLite implementation
- [ ] migration strategy
- [ ] persistence integration tests
- [ ] optional PostgreSQL implementation

Do not introduce a database before the domain contracts are understood.

---

# PHASE 5 — Engineering Tool Engine

Status: PLANNED

Goal:

Allow Bright to safely execute engineering tools.

Architecture:

    ToolEngine
        ↓
    CommandRunner
        ↓
    OutputProcessor
        ↓
    ContextBuilder
        ↓
    AIProvider

## Initial tools

- [ ] Python execution
- [ ] Git
- [ ] test runners
- [ ] filesystem inspection
- [ ] Docker
- [ ] Terraform
- [ ] AWS CLI

## Safety requirements

Every tool should have:

- explicit command boundaries
- controlled working directory
- timeout handling
- stdout capture
- stderr capture
- exit-code handling
- structured result representation

Destructive or external operations should have explicit approval boundaries.

---

# PHASE 6 — Tool Output Intelligence

Status: PLANNED

Goal:

Prevent raw command output from consuming unnecessary AI context.

Output pipeline:

    Command
       ↓
    Raw Output
       ↓
    OutputProcessor
       ↓
    Relevant Signal
       ↓
    ContextBuilder
       ↓
    AI

## OutputProcessor responsibilities

- remove repetitive output
- collapse duplicate lines
- preserve errors
- preserve warnings
- preserve actionable results
- extract test failures
- identify changed files
- identify Git state
- identify command exit status

This component should reduce context without hiding important information.

---

# PHASE 7 — Engineering Agent

Status: PLANNED

Goal:

Allow Bright to execute bounded engineering tasks autonomously.

Agent loop:

    Task
      ↓
    Inspect
      ↓
    Plan
      ↓
    Implement
      ↓
    Test
      ↓
    Diagnose
      ↓
    Repair
      ↓
    Test
      ↓
    Review
      ↓
    Complete

## Agent capabilities

- [ ] repository inspection
- [ ] code search
- [ ] dependency analysis
- [ ] task planning
- [ ] code modification
- [ ] test execution
- [ ] failure diagnosis
- [ ] bounded repair
- [ ] Git diff analysis
- [ ] documentation updates
- [ ] task completion reporting

## Agent safety

The agent must distinguish between:

### Safe autonomous operations

- reading source code
- searching the repository
- editing scoped source files
- creating tests
- running local tests
- running local Python commands
- inspecting Git state
- generating documentation

### Approval-required operations

- Git push
- destructive Git operations
- deleting important files
- modifying real learner data
- creating paid AWS infrastructure
- modifying external infrastructure
- handling credentials
- deployments
- irreversible operations

---

# PHASE 8 — Durable Memory

Status: PLANNED

Goal:

Give Bright durable engineering memory.

Potential memory categories:

- working memory
- conversation memory
- engineering decisions
- project knowledge
- learning history
- mistakes and resolutions
- user preferences
- completed tasks
- architecture decisions

Architecture:

    Bright Core
        ↓
    MemoryEngine
        ↓
    MemoryStore
        ├── LocalMemoryStore
        ├── Future external adapter
        └── Future cloud store

Memory should have explicit boundaries and should not be scattered throughout application services.

---

# PHASE 9 — Engineering Knowledge System

Status: PLANNED

Goal:

Expand Bright's structured knowledge architecture beyond the initial AWS learning framework.

Potential domains:

- AWS
- cloud engineering
- DevOps
- Terraform
- Docker
- CI/CD
- networking
- software engineering
- safety-critical engineering
- avionics
- drone systems
- embedded systems
- systems engineering

New knowledge should remain data-driven wherever practical.

---

# PHASE 10 — Project Intelligence

Status: PLANNED

Goal:

Allow Bright to understand an engineering project rather than merely execute isolated commands.

Capabilities:

- [ ] repository map
- [ ] dependency graph
- [ ] architecture understanding
- [ ] test map
- [ ] documentation map
- [ ] Git history understanding
- [ ] configuration understanding
- [ ] project health checks
- [ ] architecture drift detection

---

# PHASE 11 — Engineering Operating System

Status: LONG-TERM

The final architecture should allow Bright to coordinate:

    Knowledge
       +
    Memory
       +
    Planning
       +
    Tools
       +
    Code
       +
    Testing
       +
    Cloud
       +
    Engineering Workflows

The system should be able to receive a high-level engineering objective and decompose it into controlled tasks.

Example:

    User:
    "Build the AWS learning environment."

Bright should eventually be able to:

    understand objective
        ↓
    inspect current project
        ↓
    create execution plan
        ↓
    execute safe tasks
        ↓
    test
        ↓
    diagnose
        ↓
    request approval for external actions
        ↓
    continue
        ↓
    document result

---

# Current Priority

The immediate priority is NOT to build every future component.

The immediate priority is:

    1. Stabilize tests
    2. Clean application boundaries
    3. Establish persistence contracts
    4. Build ToolEngine
    5. Build controlled agent execution
    6. Add durable engineering memory
    7. Expand engineering knowledge
    8. Build project intelligence

Do not skip foundational architecture merely because future capabilities are more exciting.

---

# Agent Task Selection Rules

When asked to continue development:

1. Read this roadmap.
2. Find the first incomplete task in the current active phase.
3. Verify that the task is still relevant to the actual repository.
4. Inspect implementation and tests.
5. Implement the smallest complete increment.
6. Test it.
7. Stop at the review gate.

If the roadmap conflicts with the actual implementation, do not blindly follow the roadmap.

Report the conflict and propose the smallest correction.

---

# Definition of a Successful Phase

A phase is complete when:

- required behavior works
- tests are reliable
- architecture boundaries are clear
- documentation reflects reality
- no known critical regression remains
- the next phase can build on the result without rewriting the previous phase

---

# Prime Directive

Build Bright as an engineering system.

Do not optimize for feature count.

Optimize for:

    capability
    reliability
    autonomy
    safety
    clarity
    maintainability
