import json
from pathlib import Path


class KnowledgeService:

    def __init__(self):

        self.knowledge_file = Path("data/knowledge.json")

    # --------------------------------------------------
    # File Management
    # --------------------------------------------------

    def load(self) -> dict:

        if not self.knowledge_file.exists():
            return {}

        with open(
            self.knowledge_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def save(self, knowledge: dict):

        with open(
            self.knowledge_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                knowledge,
                file,
                indent=4,
                ensure_ascii=False
            )

    # --------------------------------------------------
    # Generic Storage
    # --------------------------------------------------

    def add(self, category: str, entry: dict):

        knowledge = self.load()

        if category not in knowledge:
            knowledge[category] = []

        knowledge[category].append(entry)

        self.save(knowledge)

    # --------------------------------------------------
    # Memory Processing
    # --------------------------------------------------

    def process_memory(
        self,
        classification: dict,
        message: str
    ):

        action = classification["action"]
        memory_type = classification["memory_type"]

        entry = {
            "content": message
        }

        category_map = {
            "fact": "facts",
            "goal": "goals",
            "learning": "learning",
            "project": "projects",
            "preference": "preferences",
            "task": "tasks",
            "contact": "contacts",
            "event": "events",
            "achievement": "achievements"
        }

        if action == "create":

            category = category_map.get(memory_type)

            if category:
                self.add(
                    category,
                    entry
                )

        elif action == "update":

            # BA-016
            pass

        elif action == "archive":

            # BA-017
            pass

        elif action == "delete":

            # Future
            pass

    # --------------------------------------------------
    # Generic Retrieval
    # --------------------------------------------------

    def get(self, category: str):

        knowledge = self.load()

        return knowledge.get(category, [])

    # --------------------------------------------------
    # Convenience Methods
    # --------------------------------------------------

    def get_facts(self):
        return self.get("facts")

    def get_goals(self):
        return self.get("goals")

    def get_learning(self):
        return self.get("learning")

    def get_projects(self):
        return self.get("projects")

    def get_preferences(self):
        return self.get("preferences")

    def get_tasks(self):
        return self.get("tasks")

    def get_contacts(self):
        return self.get("contacts")

    def get_events(self):
        return self.get("events")
    
    def get_achievements(self):
        return self.get("achievements")

    # --------------------------------------------------
    # Knowledge Snapshot
    # --------------------------------------------------

    def get_all(self):

        return {
            "Goals": self.get_goals(),
            "Learning": self.get_learning(),
            "Projects": self.get_projects(),
            "Facts": self.get_facts(),
            "Preferences": self.get_preferences(),
            "Tasks": self.get_tasks(),
            "Contacts": self.get_contacts(),
            "Events": self.get_events(),
            "Achievements": self.get_achievements()
        }