from dataclasses import dataclass
from typing import Any


@dataclass
class Classification:


    
    """
    Result of classifying a user message.
    """

    intent: str
    memory_type: str
    action: str
    category: str
    confidence: float
    importance: str
    source: str


    

@dataclass
class Context:


    """
    Context assembled for reasoning.
    """

    knowledge: dict[str, Any]

    learning: list[str] | None = None
    goals: list[str] | None = None
    tasks: list[str] | None = None
    



    


@dataclass
class Response:

    
    """
    Final response produced by the cognitive pipeline.
    """

    message: str



@dataclass
class Plan:

    title: str
    steps: list[str]
    

@dataclass
class Goal:
    """
    Represents an active user goal.
    """

    title: str
    status: str





@dataclass
class GoalProgress:

    """
    Responsible for tracking Goal progress
    """

    goal: str

    progress: float

    completed: list[str]

    remaining: list[str]



@dataclass
class Priority:
    """
    Represents the user's current highest priority.
    """

    title: str
    reason: str



@dataclass
class MemoryEntry:

    content: str
    category: str
    importance: str


@dataclass
class CognitiveState:

    message: str

    intent: str = ""

    classification: Classification | None = None

    context: Context | None = None

    goal: Goal | None = None

    goal_progress: GoalProgress | None = None

    priority: Priority | None = None

    plan: Plan | None = None

    response: Response | None = None

    


