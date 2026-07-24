# Bright Assistant Architecture

## Overview

Bright Assistant is an AI-powered Engineering Learning Platform.

Its purpose is to help engineers learn, practice, assess, and track progress through structured learning paths.

The architecture is intentionally modular. Each component has a single responsibility and can evolve independently.

The overall learning flow is:

Knowledge Base
↓
Loaders
↓
Engines
↓
Planning
↓
Study Session
↓
Exercises
↓
Assessments
↓
Progress
↓
Next Learning Session

---

# Design Principles

Bright follows several architectural principles.

## 1. Single Responsibility Principle

Each component has one responsibility.

Examples:

- Models represent data.
- Loaders read files.
- Engines manage collections.
- Services implement business logic.

Each layer is independent.

---

## 2. Separation of Concerns

The project separates:

Knowledge Storage

from

Business Logic

from

Application Logic.

This makes every component easier to understand, test, and replace.

---

## 3. Knowledge-Driven Architecture

Bright is driven by structured knowledge instead of hardcoded logic.

The knowledge base contains:

- Skills
- Resources
- Frameworks
- Exercises
- Assessments

The application loads this knowledge dynamically.

Adding new content should require little or no code changes.

---

# Project Structure

app/

Contains the application source code.

knowledge/

Contains structured engineering knowledge.

data/

Stores learner progress and persistent state.

tests/

Contains architecture and feature tests.

docs/

Contains project documentation.

---

# Models

Models define the application's domain objects.

Examples:

Skill

Resource

Framework

Milestone

Exercise

Assessment

StudySession

LearningPlan

AssessmentResult

ExerciseResult

Models contain data only.

They do not implement business logic.

---

# Loaders

Purpose

Loaders read structured YAML files and convert them into strongly typed models.

Examples:

SkillLoader

ResourceLoader

FrameworkLoader

ExerciseLoader

AssessmentLoader

A Loader only knows how to load one file.

It never manages collections.

Why?

Keeping loaders small makes them easy to test and reuse.

---

# Engines

Purpose

Engines manage collections of domain objects.

Examples:

SkillEngine

ExerciseEngine

AssessmentEngine

FrameworkEngine

ResourceEngine

Responsibilities

Load directories

Store objects in memory

Provide lookup methods

Hide storage implementation

Why?

The rest of the application should never need to know where data came from.

Whether the data originated from YAML, JSON, a database, or an API should not affect application logic.

---

# Two Engine Patterns

Bright currently uses two engine patterns.

## Collection Engines

These support loaders that return multiple objects from one file.

Examples:

SkillEngine

ResourceEngine

These engines iterate over collections returned by their loaders.

---

## Object Engines

These support loaders that return one object per file.

Examples:

FrameworkEngine

ExerciseEngine

AssessmentEngine

These engines inherit common behavior from BaseEngine.

This distinction exists because the knowledge base currently contains two storage patterns.

Future versions may standardize on one object per file.

---

# BaseEngine

Purpose

BaseEngine eliminates duplicated logic shared by object-based engines.

It provides:

load_directory()

get()

get_all()

Object engines expose domain-specific wrapper methods such as:

get_exercise()

get_assessment()

This keeps public APIs descriptive while minimizing duplicated implementation.

---

# Services

Services contain business logic.

Examples:

PlanningEngine

ProgressService

StudySessionService

ExerciseProgressService

Services coordinate models and engines.

They implement workflows rather than storage.

---

# Knowledge Base

The knowledge directory contains structured engineering content.

knowledge/

cloud/

skills/

resources/

frameworks/

exercises/

assessments/

The long-term goal is for new engineering courses to be added by creating YAML files rather than writing Python code.

---

# Learning Pipeline

Bright follows this learning pipeline.

Framework

↓

Planning Engine

↓

Learning Plan

↓

Study Session

↓

Resources

↓

Exercises

↓

Assessment

↓

Progress

↓

Next Milestone

Each layer builds upon the previous one.

---

# Persistence

Bright currently stores learner state using JSON.

Examples:

progress.json

exercise_progress.json

This approach keeps the project lightweight while the architecture evolves.

Future versions may migrate to a database without affecting the service layer.

---

# Future Architecture

Planned capabilities include:

Assessment grading

Adaptive learning

AI explanations

Project-based learning

Portfolio generation

Career guidance

Because Bright follows modular design principles, these features can be added without major architectural changes.

---

# Architectural Philosophy

Bright is designed as an Engineering Learning Platform rather than a collection of AI prompts.

Knowledge, planning, assessment, and progress are treated as independent systems.

This separation improves maintainability, scalability, and testability while making it easier to support new engineering disciplines in the future.