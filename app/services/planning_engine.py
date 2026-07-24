from pathlib import Path
from typing import Optional
from app.models.learning_plan import LearningPlan
from app.models.milestone import Milestone
from app.services.knowledge_engine import KnowledgeEngine
from app.services.progress_service import ProgressService

class PlanningEngine:

    def __init__(self):
        self.knowledge = KnowledgeEngine()
        self.progress = ProgressService()

    def load_framework(self, path: str | Path) -> None:
        self.knowledge.load_framework(path)

    def get_first_milestone(self) -> Optional[Milestone]:
        milestones = self.knowledge.get_milestones()

        if not milestones:
            return None
        
        return milestones[0]

    def get_next_milestone(
        self,
        completed: list[str]
    ) -> Optional[Milestone]:
        
        completed_set = set(completed)

        milestones = self.knowledge.get_milestones()

        for milestone in milestones:

            # Skip completed milestones
            if milestone.id in completed_set:
                continue

            # Return the first milestone whose dependencies are satisfied
            if all(dep in completed_set for dep in milestone.depends_on):
                return milestone

        # Framework completed
        return None
    

    def create_learning_plan(self,completed: list[str]) -> Optional[LearningPlan]:

        milestone = self.get_next_milestone(completed)

        if milestone is None:
            return None

        skills = [
            self.knowledge.get_skill(skill_id)
        for skill_id in milestone.skill_ids
    ]

        resources = [
            self.knowledge.get_resource(resource_id)
        for resource_id in milestone.resource_ids
    ]

        return LearningPlan(
        milestone=milestone,
        skills=skills,
        resources=resources
    )


    def create_learning_plan_for_framework(
        self,
        framework_id: str
    ) -> Optional[LearningPlan]:

        progress = self.progress.get_progress(framework_id)

        return self.create_learning_plan(
            progress.completed_milestones
    )