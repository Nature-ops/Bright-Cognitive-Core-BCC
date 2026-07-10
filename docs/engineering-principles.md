# Bright Assistant Engineering Standards

**Project:** Bright Assistant

**Version:** 1.0

**Last Updated:** July 2026

---

# Vision

Bright Assistant is an AI-powered engineering companion designed to help users learn, build, and grow in:

- AWS Cloud
- DevOps
- Python
- Avionics
- UAV Systems
- Robotics
- Software Engineering

The project will be developed using professional software engineering practices with emphasis on clean architecture, documentation, maintainability, and scalability.

---

# Development Philosophy

Every feature should be:

- Simple
- Maintainable
- Well documented
- Easy to test
- Easy to extend

We build software for the future, not just for today.

---

# Project Structure

```
bright-assistant/

├── app/
├── docs/
├── tests/
├── data/
├── docker/
├── README.md
├── CHANGELOG.md
├── requirements.txt
└── .gitignore
```

Every file must have a clear purpose.

---

# Folder Responsibilities

## app/

Contains all application source code.

### api/

API endpoints only.

No business logic.

### models/

Pydantic models.

Used for request validation and response serialization.

### services/

Application logic.

No API routes.

### database/

Database connections and queries.

### prompts/

System prompts and AI prompt templates.

### config/

Application configuration.

### utils/

Reusable helper functions.

---

# Documentation Standards

Every sprint must update:

- README.md
- CHANGELOG.md

Every major feature should include documentation inside:

docs/

---

# Git Standards

Every completed feature requires a Git commit.

Commit message format:

```
feat:
fix:
docs:
refactor:
test:
style:
chore:
```

Examples:

```
feat: add chat endpoint

docs: update project standards

fix: correct chat validation
```

---

# Coding Standards

- Use meaningful variable names.
- Keep functions small.
- Avoid duplicated code.
- Write readable code before clever code.
- Keep comments useful.
- Remove unused code.

---

# FastAPI Standards

Each endpoint should include:

- Request model
- Response model
- Proper status codes
- Documentation

Business logic should not live inside API routes.

---

# Documentation Rules

Every new feature should answer:

- What was added?
- Why was it added?
- How does it work?

---

# Testing Philosophy

Every major feature should eventually include tests.

Tests belong inside:

```
tests/
```

---

# AI Development Rules

The AI should:

- Teach rather than simply answer.
- Explain engineering concepts.
- Encourage practical implementation.
- Generate quizzes.
- Recommend projects.
- Track learning progress.

---

# AWS Integration Rules

Whenever possible, new AWS knowledge should be integrated into Bright Assistant.

Examples:

IAM → Authentication

S3 → Document Storage

CloudWatch → Monitoring

Lambda → Background Tasks

DynamoDB → User Memory

API Gateway → Public API

---

# UAV Integration Rules

Future drone modules should support:

- PX4
- MAVLink
- ROS2
- Drone Telemetry
- Flight Logs
- Mission Planning

---

# Development Workflow

Every sprint follows this process:

1. Plan
2. Design
3. Implement
4. Test
5. Document
6. Commit
7. Push

---

# Core Principle

Bright Assistant is not just an AI chatbot.

It is an Engineering Companion.

Every decision made in this project should support that vision.
## Architecture Rule

API routes should never contain business logic.

Routes receive requests.

Services perform work.

Models define data.

Main creates the application.
## Engineering Checklist

Before implementing any feature:

- [ ] What responsibility does this feature have?
- [ ] Which service owns it?
- [ ] Will this still make sense one year from now?
- [ ] Does it follow the Single Responsibility Principle?
- [ ] Can another module reuse it?
- [ ] If this component changed tomorrow, what would break?

# Bright Engineering Principles

## 1. Single Responsibility

Every service should have one clear responsibility.

---

## 2. Architecture Before Implementation

Design first.
Implement second.

---

## 3. Never Ask the LLM What Bright Already Knows

If information exists inside Bright's knowledge base,
retrieve it before calling the language model.

---

## 4. Prefer Simple Solutions

Start with the simplest implementation that solves the problem.

Complexity must be earned.

---

## 5. Modular Design

Every service should be replaceable without changing the rest of the platform.

---

## 6. Build for the Long Term

Every architectural decision should still make sense one year from now.