# Changelog

---

## v0.1.0 - Project Foundation

### Added

- Initialized the Bright Assistant GitHub repository.
- Created the Python virtual environment.
- Installed FastAPI and Uvicorn.
- Created the initial project structure.
- Added the root (`/`) endpoint.
- Added the health (`/health`) endpoint.
- Verified the application runs locally.

---

## v0.2.0 - Modular API Architecture

### Added

- Created the `api` module.
- Created the `services` module.
- Added the `ChatService` class.
- Added the `/chat` endpoint.
- Added request and response models.
- Separated API routes from business logic.
- Added Swagger API testing support.
- Created the initial project documentation.
## v0.3.0 - Configuration Layer

### Added

- Created centralized application settings.
- Added `.env` configuration support.
- Added `.env.example`.
- Configured FastAPI to use centralized settings.
- Prepared the project for environment-based configuration.
## v0.6.0 - AI Provider Architecture

### Added

- Created AI provider abstraction.
- Added BaseAIProvider interface.
- Added Ollama provider implementation.
- Connected ChatService to PromptService.
- Connected PromptService to AI Provider.
- Simulated AI responses using provider architecture.
## v0.2.0 - Local AI & Memory

### Added

- Integrated Ollama with Bright Assistant.
- Added local Llama and Qwen model support.
- Implemented AI provider abstraction.
- Created PromptService.
- Added dynamic prompt loading.
- Implemented MemoryService.
- Added persistent conversation storage.
- Improved logging throughout ChatService.
- Organized prompt library.
- Updated project documentation.
- Added Bright Care to the long-term product vision.

### Improved

- Modular project architecture.
- Local AI response generation.
- Configuration management.

## v0.3.0 - Contextual Memory

### Added

- MemoryService for persistent conversation storage.
- ConversationService to build AI conversations.
- ChatService refactored into a coordinator.
- OllamaProvider updated to support full chat history.
- Bright now remembers previous conversations within stored history.


## v0.4.0 - Knowledge Engine Foundation

### Added

- MemoryClassifier service
- KnowledgeService
- Structured knowledge storage
- knowledge.json
- Memory architecture documentation
- Knowledge architecture documentation
- Rule-based memory classification
- Automatic knowledge persistence

### Improved

- Separated conversation memory from structured knowledge.
- Refactored Bright architecture toward a modular knowledge engine.
- Strengthened service-based architecture.

### Documentation

- Added memory-architecture.md
- Added knowledge-architecture.md
- Updated Engineering Notebook


## v0.4.1 - Knowledge Retrieval

### Added

- Generic knowledge retrieval method
- Learning retrieval
- Goal retrieval
- Project retrieval
- Fact retrieval
- Preference retrieval
- Task retrieval

### Improved

- Refactored KnowledgeService to reduce duplicate code.
- Updated knowledge storage to use structured objects.
- Bright now retrieves learning information directly from its knowledge base.

### Fixed

- Corrected knowledge storage format.
- Fixed retrieval logic for structured knowledge entries.
- Fixed ChatService knowledge lookup workflow.


## BCC-004 - Memory Evolution Foundation

### Added

- Bright Cognitive Core architecture
- Memory Evolution Engine
- Reasoning Service integration
- Generic knowledge processing
- Generic knowledge storage

### Improved

- Refactored MemoryClassifier to support:
  - intent
  - action
  - confidence
  - importance
  - category
- Simplified KnowledgeService
- Reduced duplicated storage code
- Refactored ChatService into an orchestration layer

### Architecture

Introduced the Bright Cognitive Core.

Current cognitive pipeline:

MemoryClassifier

↓

MemoryEvolutionEngine

↓

KnowledgeService

↓

ReasoningService

↓

ConversationService

↓

AI Provider

## v0.5.1-alpha

### Added

- Reflection Engine
- Reflection Rules
- Insight model
- Insight Service
- Insights datastore
- Cognitive reflection architecture

### Improved

- Continued CognitiveState migration
- Expanded Bright Cognitive Core

## Sprint Summary

Completed Reflection Engine v1.

Bright can now:

- Detect achievements.
- Create insights.
- Persist insights.
- Build higher-level knowledge from memories.

Reflection follows the standard pattern:

process()
→ detect()
→ create()
→ store()
→ return state


## BCC-010 - Cognitive Pipeline

### Added

- Introduced CognitivePipeline.
- Migrated Intent Routing into the pipeline.
- Migrated Memory Classification into the pipeline.
- Migrated Memory Evolution into the pipeline.
- Added Classification source tracking.
- Improved engine responsibility separation.

### Refactored

- ChatService now delegates cognitive processing to the pipeline.
- Reduced ChatService complexity.


# BCC-013 — Bright Cognitive Core v1

**Date:** 2026-07-14

## Added

- ContextEngine integrated into the Cognitive Pipeline.
- ReasoningEngine integrated into the Cognitive Pipeline.
- Standardized cognitive engines using `process(state)`.
- Pipeline now produces responses through `state.response`.

## Changed

- Migrated KnowledgeEngine into the Cognitive Pipeline.
- Migrated ReflectionEngine into the Cognitive Pipeline.
- Migrated ContextEngine into the Cognitive Pipeline.
- Migrated ReasoningEngine into the Cognitive Pipeline.
- Simplified ChatService responsibilities.

## Improved

- Established a unified cognitive workflow.
- Standardized engine interfaces.
- Reduced coupling between ChatService and cognitive logic.
- Improved maintainability and extensibility.

## Architecture

Bright Cognitive Core v1 completed.

Current cognitive execution order:

Intent Router
→ Memory Classifier
→ Memory Evolution
→ Knowledge Engine
→ Reflection Engine
→ Context Engine
→ Reasoning Engine

# Changelog

All notable changes to Bright Assistant are documented in this file.

The format follows the principles of Keep a Changelog.

---

## [Unreleased]

### Added

#### Cognitive Core

- Added GoalEngine to detect the user's active goal.
- Added PriorityEngine to determine the user's current priority.
- Added Priority dataclass to CognitiveState.
- Added Goal dataclass to CognitiveState.

#### Planning

- PlanningEngine now uses the active Priority instead of directly using the Goal.
- Planning rules continue to generate dynamic learning plans.

#### Memory

- Added duplicate detection to KnowledgeService.
- Prevented duplicate knowledge entries from being stored.
- Added logging for duplicate memory detection.

#### Architecture

- Extended the Cognitive Pipeline with:
  - GoalEngine
  - PriorityEngine
- Improved separation of responsibilities between cognitive engines.

#### Documentation

- Created VISION.md.
- Created MILESTONES.md.
- Updated Engineering Notebook.

## BCC-020 - Goal Progress Engine

### Added
- GoalProgress dataclass
- ProgressEngine
- Goal progress tracking
- Progress-aware PriorityEngine

### Changed
- ReasoningEngine now reports goal progress.
- PlanningEngine removes duplicate planning steps.
- Cognitive pipeline includes ProgressEngine.

### Fixed
- Duplicate knowledge entries.
- Duplicate planning recommendations.

## [BCC-022A] - Knowledge Framework Design

### Added

- Designed Bright Knowledge Layer architecture.
- Added `knowledge/` directory.
- Added domain organization:
  - Cloud
  - Drones
  - Logistics
  - Software
  - Business
  - Personal
- Defined Bright Knowledge Standard (BKS).
- Added architecture documentation for knowledge frameworks.

### Planned

- Framework models
- Framework loader
- YAML validation

## BCC-022

### Added

- Knowledge Layer architecture
- Framework model
- GoalTemplate model
- Milestone model
- Skill model
- Resource model
- FrameworkLoader
- KnowledgeEngine
- AWS reference framework


# Changelog

## [Unreleased]

### Added

- Implemented `Progress` domain model for tracking learner progress.
- Added `ProgressService` with persistent JSON storage.
- Added support for:
  - `get_progress()`
  - `update_progress()`
  - `complete_milestone()`
- Added `tests/test_progress_service.py`.
- Integrated `PlanningEngine` with `ProgressService`.
- Added automatic generation of learning plans based on saved learner progress.
- Improved learning plan output with resolved Skill and Resource objects.
- Expanded AWS framework with foundational AWS Fundamentals skills.
- Added new AWS skill catalog entries:
  - Cloud Basics
  - AWS Global Infrastructure
  - Shared Responsibility Model

### Changed

- `PlanningEngine` can now generate learning plans directly from learner progress.
- Learning plans now automatically continue from the learner's last completed milestone.

### Fixed

- Fixed milestone YAML structure.
- Fixed skill catalog definitions.
- Corrected milestone skill/resource resolution.
- Fixed LearningPlan generation for AWS Fundamentals.


# Changelog

## [Sprint 32] - 2026-07-24

### Added
- Implemented `StudySession` model to represent a complete learning session.
- Added `Objective` model for structured learning objectives.
- Implemented `StudySessionService` to orchestrate study session creation.
- Added objective generation from LearningPlan skills.
- Added exercise integration using ExerciseEngine.
- Added resource integration using LearningPlan resources.
- Added optional assessment support for milestones.
- Added estimated study time calculation.
- Created end-to-end integration test for study sessions.

### Changed
- Refactored `StudySession` to embed `LearningPlan` instead of duplicating framework and milestone data.
- Renamed milestone collection fields to maintain naming consistency (`skill_ids`, `resource_ids`, `exercise_ids`).
- Updated assessment workflow to support milestones without assessments.

### Fixed
- Resolved milestone validation issues caused by optional assessment IDs.
- Fixed assessment lookup failures for milestones without assessments.
- Verified complete study session generation pipeline.