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

    knowledge: dict[str, Any]

    learning: list[str] | None = None
    goals: list[str] | None = None
    tasks: list[str] | None = None
    



    """
    Context assembled for reasoning.
    """


@dataclass
class Response:

    message: str

    """
    Final response produced by the cognitive pipeline.
    """


@dataclass
class Plan:

    title: str
    steps: list[str]
    


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

    plan: Plan | None = None

    response: Response | None = None