# Bright Assistant — Agent Instructions

## 1. Mission

Bright Assistant, also referred to as Bright Cognitive Core (BCC), is an AI-powered Engineering Operating System.

Bright is being built to help engineers:

- learn engineering subjects
- follow structured learning paths
- practice through exercises
- complete assessments
- track learning progress
- build engineering projects
- automate engineering workflows
- interact with engineering tools
- develop technical knowledge
- eventually receive intelligent engineering assistance

The long-term goal is not merely a chatbot.

Bright should become an engineering system capable of understanding projects, executing controlled engineering workflows, learning from results, and helping engineers build real systems.

---

# 2. Engineering Philosophy

Bright must prioritize:

1. Correctness
2. Maintainability
3. Testability
4. Clear architecture
5. Small composable components
6. Explicit boundaries
7. Data-driven behavior
8. Safe automation
9. Backward compatibility
10. Incremental evolution

Do not optimize for writing the most code.

Optimize for creating the smallest correct change that moves the architecture forward.

---

# 3. Current Architecture

The current application contains two primary surfaces.

## FastAPI surface

The backend is centered around:

    app/main.py

It exposes application functionality including:

- chat
- prompt handling
- memory
- health endpoints

The AI provider architecture is modular.

---

## CLI learning surface

The learning workflow is driven by:

    BrightCLI
        ↓
    SessionController
        ↓
    StudyEngine
        ↓
    StudySession
        ↓
    LearningPlan
        ↓
    Framework / Milestone content

The learning pipeline is:

    Knowledge YAML
        ↓
    Loaders
        ↓
    Engines
        ↓
    Planning
        ↓
    LearningPlan
        ↓
    StudySession
        ↓
    Objectives
        ↓
    Exercises
        ↓
    Assessment
        ↓
    Progress
        ↓
    Next Milestone

---

# 4. Knowledge Architecture

Structured engineering knowledge lives under:

    knowledge/

Current categories include:

    cloud/
        skills/
        resources/
        frameworks/
        exercises/
        assessments/

Knowledge should remain data-driven whenever practical.

Adding a learning milestone should generally require YAML/data changes rather than hardcoded Python logic.

Do not hardcode course-specific behavior into engines or the CLI unless there is a strong architectural reason.

---

# 5. Domain Models

Domain models live under:

    app/models/

Important models include:

- Framework
- Milestone
- Skill
- Resource
- Exercise
- Assessment
- LearningPlan
- StudySession
- StudyProgress
- Progress
- AssessmentResult
- ExerciseResult

Models represent domain data.

Avoid placing application workflows inside models.

---

# 6. Engines

Engines live under:

    app/services/

Important engines include:

- KnowledgeEngine
- PlanningEngine
- ResourceEngine
- ExerciseEngine
- AssessmentEngine
- StudyEngine

Engines should own domain behavior appropriate to their responsibility.

Do not allow UI code to reach deeply into engine internals when a controller/API method can expose the required behavior.

Preferred:

    CLI
      ↓
    Controller API

Avoid:

    CLI
      ↓
    Controller
      ↓
    Engine internal service
      ↓
    Persistence implementation

Public boundaries should be explicit.

---

# 7. SessionController

SessionController is the composition and orchestration boundary for the CLI learning workflow.

It is responsible for exposing learning operations to the CLI without requiring the CLI to understand internal service composition.

The CLI should communicate with the controller rather than reaching through the controller into engine internals.

Recent architectural cleanup introduced methods such as:

    completed_milestones()

The principle is:

    CLI
      ↓
    SessionController
      ↓
    internal services/engines

---

# 8. Current Progress Architecture

Bright currently uses JSON persistence.

Framework progress:

    data/progress.json

Study-session progress:

    data/study_progress/

There is also an older exercise persistence service:

    data/exercise_progress.json

The active StudyEngine workflow currently uses StudyProgressService for session state.

ExerciseProgressService is currently not part of the active StudyEngine execution path.

Do not remove or redesign ExerciseProgressService unless a roadmap task explicitly requires it.

---

# 9. Critical Data Safety Rule

Never modify real learner progress merely to make a test pass.

Never casually modify:

    data/progress.json

Never delete:

    data/study_progress/

to obtain a convenient test state.

Tests requiring different progress states must use:

- temporary directories
- temporary JSON files
- dependency injection
- controlled test fixtures
- mocks/patches where appropriate

Real learner progress must remain untouched during automated testing.

---

# 10. Microsoft Directory

The repository may contain an untracked:

    Microsoft/

directory created by PowerShell tooling.

Do not:

- delete it
- modify it
- add it to Git
- include it in commits

unless explicitly instructed by the user.

It is unrelated to Bright application development.

---

# 11. Testing Rules

Before considering a change complete:

1. Compile changed Python files.
2. Run relevant existing tests.
3. Run newly created tests.
4. Run integration tests when behavior crosses components.
5. Check Git diff.
6. Run:

    git diff --check

Tests must not depend on the user's real persistent learning state unless explicitly testing that state.

Prefer isolated temporary state for integration tests.

Do not introduce pytest merely for convenience if the project can test the feature with the existing environment.

Use the project's existing testing conventions unless there is a clear reason to improve them.

---

# 12. Test Independence

A test must not rely on:

- another test having run first
- repository data accidentally containing a particular milestone
- a previous interactive session
- a developer's local state

Tests should establish their required state explicitly.

If a test needs IAM to be the next milestone, create that state in temporary storage.

---

# 13. Git Safety

Never commit automatically unless explicitly instructed.

Never push automatically unless explicitly instructed.

Before committing:

    git status
    git diff
    git diff --check

Never include unrelated files in a commit.

Never stage:

    Microsoft/

unless explicitly instructed.

Do not use destructive commands such as:

    git reset --hard
    git clean -fd
    git checkout .

unless explicitly authorized.

When reverting work, restore only the files known to belong to the requested change.

---

# 14. Change Scope

Every task must have a clearly defined scope.

Prefer:

    one architectural objective
    +
    minimum required files
    +
    tests

Avoid broad opportunistic refactoring.

Do not modify unrelated files because they appear imperfect.

Do not reformat entire files unless formatting is the task.

Do not rename components unless required.

Do not change public behavior unless explicitly requested.

---

# 15. Inspect Before Editing

Before modifying code:

1. Inspect the relevant implementation.
2. Inspect its callers.
3. Inspect relevant tests.
4. Understand current behavior.
5. Check Git status.
6. Identify persistence/state implications.

Never infer architecture from a single file.

Use repository search to identify actual dependencies.

---

# 16. Preserve Existing Behavior

Architectural improvements must preserve existing behavior unless behavior change is explicitly part of the task.

Important existing behavior includes:

- dependency-aware milestone selection
- deterministic milestone ordering
- resumable study sessions
- objective progression
- exercise progression
- assessment scoring
- assessment passing threshold
- milestone completion
- automatic progression to the next milestone
- final framework completion
- CLI progress display

Regression tests are required when modifying these areas.

---

# 17. Milestone Progression

The learning framework uses dependency-aware progression.

PlanningEngine selects the first incomplete milestone whose dependencies are satisfied.

Framework YAML ordering determines deterministic selection among eligible milestones.

When a milestone is successfully completed:

    StudyEngine
        ↓
    framework progress persistence

Then:

    PlanningEngine
        ↓
    next eligible milestone

Automatic progression must not:

- duplicate completed milestones
- skip milestones
- bypass dependencies
- lose session state
- modify unrelated framework state

---

# 18. Completion Semantics

A study session is complete only when:

- all required objectives are completed
- all required exercises are completed
- the required assessment is completed successfully, if one exists

Do not mark a milestone complete merely because an assessment was attempted.

Passing the assessment is not itself the entire completion operation.

The controller's completion/transition API must preserve these semantics.

---

# 19. Persistence Architecture Direction

The current JSON persistence architecture is intentionally transitional.

Long-term direction:

    Domain/Application
          ↓
    Repository Boundary
          ↓
    Persistence Implementation
          ↓
    JSON / SQLite / PostgreSQL

However, do not introduce repositories, databases, or broad persistence rewrites unless the current roadmap explicitly calls for them.

Architecture must evolve incrementally.

Do not migrate to SQLite simply because it is available.

---

# 20. Future Engineering Agent

Bright will eventually gain an engineering automation architecture.

Planned direction:

    ToolEngine
        ↓
    CommandRunner
        ↓
    OutputProcessor
        ↓
    ContextBuilder
        ↓
    AIProvider

The ToolEngine will eventually support tools such as:

- Git
- Python
- Docker
- Terraform
- AWS CLI
- test runners
- system commands

Raw tool output should not automatically be passed to the AI.

The output processor should preserve:

- errors
- warnings
- important results
- actionable information

while removing:

- repetitive output
- irrelevant logs
- duplicated information

---

# 21. Agent Operating Loop

For implementation tasks, follow this loop:

    1. Read AGENTS.md
    2. Read BUILD_ROADMAP.md
    3. Inspect Git state
    4. Identify the current task
    5. Inspect relevant code
    6. Inspect relevant tests
    7. Form an implementation plan
    8. Make the smallest correct change
    9. Run focused tests
    10. Diagnose failures
    11. Fix only task-related failures
    12. Run regression tests
    13. Inspect diff
    14. Run git diff --check
    15. Stop at the review gate

Do not continue into unrelated improvements.

---

# 22. Autonomous Repair

If a test fails:

1. Determine whether the failure is caused by the current change.
2. Inspect the failure.
3. Make the smallest correction.
4. Re-run the failed test.
5. Re-run relevant regression tests.

Do not rewrite unrelated architecture simply because a test fails.

If the failure appears unrelated to the task, report it rather than changing unrelated code.

---

# 23. Stop Conditions

Stop and ask for human direction when:

- requirements conflict
- the requested architecture would break existing behavior
- real learner data would need modification
- credentials or secrets are required
- external infrastructure would be modified
- AWS resources would be created or deleted
- destructive Git operations appear necessary
- a task expands beyond its stated scope
- a large refactor becomes necessary to complete a small task
- an existing architectural assumption appears incorrect
- tests cannot safely isolate required state

Do not improvise around a safety boundary.

---

# 24. Secrets

Never expose or commit:

- passwords
- API keys
- AWS credentials
- private tokens
- authentication cookies
- private keys
- `.env` secrets

Do not print secrets into test output.

---

# 25. AWS Safety

Bright will eventually interact with AWS.

Until explicitly authorized:

- do not create paid infrastructure
- do not delete infrastructure
- do not modify production resources
- do not use unknown credentials
- do not perform billing-affecting actions

Local simulations and isolated tests are preferred.

---

# 26. Documentation

When architecture changes materially, update the appropriate documentation.

Do not modify documentation merely to hide an implementation problem.

Documentation should describe the actual architecture, not the intended architecture if the implementation does not yet support it.

---

# 27. Commit Quality

A good commit should represent one coherent change.

Preferred pattern:

    feature implementation
    +
    relevant tests
    +
    required documentation

Avoid commits containing unrelated cleanup.

Commit messages should describe the architectural or behavioral change.

---

# 28. Definition of Done

A task is complete when:

- the requested behavior is implemented
- relevant tests pass
- no unrelated behavior changed
- no unintended files changed
- no real learner state was modified
- `git diff --check` passes
- the diff is understandable
- the roadmap can be updated if necessary
- the agent stops at the review gate

The agent must not commit or push unless explicitly authorized.

---

# 29. Prime Directive

Do not make Bright merely larger.

Make Bright:

    clearer
    safer
    more modular
    more testable
    more autonomous
    more useful

Every architectural change should make future engineering work easier rather than harder.