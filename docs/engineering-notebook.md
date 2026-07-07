# Engineering Notebook

## 2026-07-05

Today I learned:

- FastAPI
- GET endpoints
- POST endpoints
- Pydantic Models

Questions I still have:

- Difference between Request and Response models.

Ideas:

- Bright Assistant should remember AWS mistakes.

# Engineering Notebook

## Date

2026-07-05

---

## Topic

FastAPI Basics

---

## Objective

Understand how FastAPI creates web APIs.

---

## What I Learned

- What FastAPI is.
- Difference between GET and POST.
- What Uvicorn does.
- What Pydantic models are.

---

## Challenges

- Typed Python code into PowerShell instead of the editor.
- Learned the difference between the editor and the terminal.

---

## Solution

Python code belongs in `.py` files.

PowerShell is only for commands.

---

## Questions

- How does FastAPI know which endpoint to execute?

---

## Next Topic

API Routers

# Engineering Notebook

---

## Date

2026-07-06

---

## Sprint

BA-002

---

## Topic

Building a Modular FastAPI Backend

---

## Objective

Learn how to organize a FastAPI application using a professional software architecture.

---

## What I Learned

### FastAPI

- FastAPI creates the web application.
- Uvicorn runs the FastAPI server.
- Swagger automatically documents API endpoints.

### API Routers

- API routes should be grouped by feature.
- Each router has one responsibility.
- Routers are connected to the application using `include_router()`.

### Pydantic Models

- Request models validate incoming data.
- Response models define outgoing data.
- FastAPI performs validation automatically.

### Service Layer

- Business logic should not live inside API routes.
- Routes should call services.
- Services perform the actual work.

### Project Organization

Today I learned that organizing code is just as important as writing code.

Keeping related code inside dedicated folders makes the application easier to maintain as it grows.

---

## Challenges

- I accidentally typed Python code into the PowerShell terminal instead of placing it inside a Python file.
- I learned the difference between the terminal and the code editor.
- I initially organized a few folders incorrectly and later corrected the structure.

---

## Solutions

- Python code belongs inside `.py` files.
- The terminal is used to execute commands.
- Every file should have one clear responsibility.

---

## Architecture Decisions

We decided that:

- `main.py` should remain small.
- API routes belong in `app/api`.
- Business logic belongs in `app/services`.
- Models belong in `app/models`.

---

## Questions

- How will multiple routers communicate?
- How will dependency injection work in FastAPI?

---

## Next Goal

Create a configuration layer using `settings.py`.

Then connect Bright Assistant to a real AI model.


## Topic

Configuration Management

### What I Learned

- Applications should not hardcode configuration values.
- Environment variables allow different configurations for development, testing, and production.
- `BaseSettings` loads configuration automatically.
- `.env` stores local configuration.
- `.env.example` documents required configuration without exposing secrets.

### Why It Matters

A professional application should be configurable without changing the source code.

### Challenges

- Learned where `.env` should be stored.
- Learned how FastAPI loads application settings.

### Next Goal

Build a logging system for Bright Assistant.

## Topic

AI Provider Architecture

### What I Learned

Today I learned that the application should never depend directly on an AI provider.

Instead, ChatService depends on an abstract provider.

Different AI models can later be swapped without changing the application.

### Key Concepts

- Abstraction
- Interfaces
- Separation of concerns
- Dependency inversion
- Strategy Pattern

### Biggest Lesson

Build for change.

Software should be easy to extend without rewriting existing code.

# Engineering Notebook

## Date
2026-07-08

---

# Session Goal

Continue building Bright Assistant into a modular AI Engineering Operating System by integrating a local Large Language Model (LLM), persistent memory, and improving the software architecture.

---

# Accomplishments

## AI Provider Integration

- Installed and configured Ollama.
- Installed the official Ollama Python package.
- Downloaded and tested:
  - Llama 3.1 8B
  - Qwen3 8B
- Connected Bright Assistant to a local LLM through the Ollama API.
- Removed the simulated responses and replaced them with real AI-generated responses.

---

## AI Architecture

Created a provider-based architecture.

```
BaseAIProvider
      │
      ├── OllamaProvider
      ├── OpenAIProvider
      ├── BedrockProvider
      └── AnthropicProvider
```

This architecture allows Bright Assistant to support multiple AI providers without changing the rest of the application.

---

## Prompt Management

Created a centralized PromptService.

Organized prompts inside:

app/prompts/

Current prompts include:

- system_prompt.txt
- coding_prompt.txt
- aws_tutor.txt
- devops_tutor.txt
- drone_engineer.txt
- python_mentor.txt
- affiliate_marketing.txt
- trading_assistant.txt
- career_coach.txt
- summarizer_prompt.txt

Bright can now load prompts dynamically.

---

## Conversation Memory

Implemented MemoryService.

Features:

- Persistent JSON conversation storage
- Conversation history loading
- Conversation saving
- Memory clearing
- Fault tolerance for invalid JSON

Conversation history is stored in:

data/conversation.json

---

## Logging

Improved logging throughout ChatService.

Current logging includes:

- Incoming user messages
- Prompt loading
- AI response generation
- Memory updates

Logs are stored in:

data/logs/bright_assistant.log

---

## Chat Pipeline

Current execution flow:

User

↓

FastAPI

↓

ChatService

↓

MemoryService (save user)

↓

PromptService

↓

OllamaProvider

↓

Local LLM (Llama / Qwen)

↓

MemoryService (save assistant)

↓

Response

---

## Documentation

Updated:

- CHANGELOG.md
- README.md
- Project Vision
- Engineering Notebook

Committed and pushed all changes to GitHub.

---

# Lessons Learned

- Build software using small, modular services.
- Separate prompts from business logic.
- Design for future AI providers from the beginning.
- Good logging makes debugging significantly easier.
- Persistent memory should be implemented before long-term reasoning.
- Clean architecture reduces future technical debt.

---

# New Product Vision

Brainstormed a future product named:

## Bright Care

An AI companion for elderly care.

Potential capabilities:

- Medication reminders
- Birthday reminders
- Voice companionship
- Reading books aloud
- Calling family members
- Wellness check-ins
- Memory exercises
- Daily scheduling
- Staff documentation assistance
- Patient status summaries
- Shift reporting

Core principle:

> Bright Care assists caregivers—it does not replace professional medical judgment.

---

# Current Project Status

Version: 0.2

Current capabilities:

✅ FastAPI Backend

✅ Local LLM

✅ Modular AI Providers

✅ Prompt Management

✅ Logging

✅ Configuration Management

✅ Persistent Memory

✅ Conversation Storage

---

# Next Session Goals

1. Feed conversation history into the LLM.
2. Build contextual memory retrieval.
3. Improve MemoryService with timestamps.
4. Begin designing long-term memory.
5. Continue evolving Bright into an Engineering Operating System.

---

# Personal Reflection

Today marked the transition of Bright Assistant from a simple chatbot into a real AI platform.

The architecture is becoming stable, modular, and scalable. The project now has a solid foundation for future features including RAG, autonomous agents, cloud integration, and specialized AI assistants such as Bright Care.