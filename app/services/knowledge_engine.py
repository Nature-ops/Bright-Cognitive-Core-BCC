from pathlib import Path
from typing import Optional
from app.models.framework import Framework
from app.models.milestone import Milestone
from app.models.resource import Resource
from app.models.skill import Skill
from app.services.framework_loader import FrameworkLoader
from app.services.resource_loader import ResourceLoader
from app.services.skill_loader import SkillLoader


class KnowledgeEngine:
    def __init__(self):
        self._framework: Framework | None = None
        self._skills: dict[str, Skill] = {}
        self._resources: dict[str, Resource] = {}

    def load_framework(self, framework_path: str | Path):
        framework_path = Path(framework_path)

        self._framework = FrameworkLoader.load(framework_path)

        knowledge_root = framework_path.parent.parent

        skills = SkillLoader.load(
            knowledge_root / "skills" / self._framework.skill_catalog
        )

        self._skills = {
            skill.id: skill
            for skill in skills
        }

        resources = ResourceLoader.load(
        knowledge_root / "resources" / self._framework.resource_catalog
        )

        self._resources = {
            resource.id: resource
            for resource in resources
        }



    def get_skill(self, skill_id: str) -> Skill:
        skill = self._skills.get(skill_id)

        if skill is None:
            raise KeyError(f"Unknown skill: {skill_id}")

        return skill
         

    def get_resource(self, resource_id: str) -> Resource:
        resource = self._resources.get(resource_id)

        if resource is None:
            raise KeyError(f"Unknown resource: {resource_id}")

        return resource
    

         
    
        

    def get_framework(self) -> Framework:
        """Return the currently loaded framework."""
        self._ensure_framework_loaded()
        assert self._framework is not None
        return self._framework

    def get_milestones(self) -> list[Milestone]:
        """Return all milestones in the loaded framework."""
        framework = self.get_framework()
        return framework.milestones

    def get_milestone(self, milestone_id: str) -> Optional[Milestone]:
        """Return a milestone by its ID."""
        self._ensure_framework_loaded()

        framework = self.get_framework()
        for milestone in framework.milestones:
            if milestone.id == milestone_id:
                return milestone

        return None
    
    def get_skills(self) -> list[Skill]:
        return list(self._skills.values())

    

    def get_resources(self) -> list[Resource]:
        return list(self._resources.values())

   



    def _ensure_framework_loaded(self) -> None:
        """Raise an error if no framework has been loaded."""
        if self._framework is None:
            raise RuntimeError("No framework has been loaded.")


    @property
    def framework(self) -> Framework:

        if self._framework is None:
            raise RuntimeError(
            "No framework has been loaded."
        )

        return self._framework


    
        
    