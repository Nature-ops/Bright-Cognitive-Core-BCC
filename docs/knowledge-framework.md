A Knowledge Framework defines a structured path for achieving a goal.

It contains:

- Goal
- Milestones
- Skills
- Dependencies
- Completion criteria

AWS Solutions Architect

Goal
│
├── AWS Fundamentals
├── IAM
├── EC2
├── S3
├── VPC
├── Route53
├── CloudFormation
├── Terraform
└── Practice Projects

# BCC-022A — Knowledge Framework Design

## Status

**Design Phase**

---

# Purpose

The Knowledge Framework provides Bright with a structured understanding of
how knowledge is organized.

Instead of storing isolated facts, Bright understands:

- what a user is trying to learn
- the milestones required to achieve the goal
- dependencies between milestones
- skills gained from each milestone
- how progress is calculated

The framework becomes the foundation for:

- Goal Progress Engine
- Planning Engine
- Priority Engine
- Reasoning Engine
- Future Reflection Engine
- Adaptive Learning

---

# Design Philosophy

Bright does not simply remember information.

Bright understands learning.

A Goal answers:

> What does the user want to achieve?

A Knowledge Framework answers:

> How does the user achieve it?

Example:

Goal

Become an AWS Solutions Architect

Knowledge Framework

AWS Fundamentals
↓

IAM
↓

EC2
↓

S3
↓

VPC
↓

CloudFormation
↓

Terraform
↓

Projects
↓

Certification

---

# Core Architecture
```

```text
Knowledge Framework
│
├── Domain
│
├── Framework
│
├── Milestones
│
├── Skills
│
├── Dependencies
│
└── Completion Rules
```

# Domain Model

The Knowledge Framework is built from a hierarchy of reusable entities.

```text
Domain
│
├── Framework
│     │
│     ├── Milestones
│     │      │
│     │      ├── Skills
│     │      ├── Dependencies
│     │      └── Completion Rules
│     │
│     └── Metadata
│
└── Learning Paths (Future)
```

Each entity has a single responsibility.

| Entity | Responsibility |
|---------|----------------|
| Domain | Groups related knowledge frameworks |
| Framework | Defines the roadmap for achieving a learning objective |
| Milestone | Represents one major learning objective |
| Skill | Represents an individual competency |
| Dependency | Defines prerequisite milestones |
| Completion Rule | Defines when a milestone is complete |

# Framework Metadata

Each framework contains descriptive information.

Example

Name:
AWS Solutions Architect Associate

Version:
2026

Author:
Bright

Difficulty:
Intermediate

Estimated Duration:
6 Months

Tags:

- AWS
- Cloud
- DevOps

Description:

Prepares learners for the AWS Solutions Architect Associate certification.

# Knowledge Directory

Bright stores knowledge as structured data.

The application contains no domain-specific knowledge.

Instead, the application loads knowledge from the `knowledge/`
directory.

```text
knowledge/
│
├── domains/
│
├── frameworks/
│
├── skills/
│
├── resources/
│
├── templates/
│
└── schemas/
```

Every directory has a single responsibility.

| Directory | Purpose |
|------------|----------|
| domains | Broad knowledge categories |
| frameworks | Learning roadmaps |
| skills | Reusable skill definitions |
| resources | Learning materials |
| templates | Goal and workflow templates |
| schemas | Validation schemas |