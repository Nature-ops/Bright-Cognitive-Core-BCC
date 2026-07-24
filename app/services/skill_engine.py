from pathlib import Path

from app.models.skill import Skill
from app.services.skill_loader import SkillLoader


class SkillEngine:

    def __init__(self):

        self._skills: dict[str, Skill] = {}

    def load_directory(self, directory: str | Path):

        for file in Path(directory).glob("*.yaml"):

            skills = SkillLoader.load(file)

            for skill in skills:

                if skill.id in self._skills:
                    raise ValueError(
                        f"Duplicate skill id: {skill.id}"
                    )

                self._skills[skill.id] = skill

    def get_skill(
        self,
        skill_id: str
    ) -> Skill:

        return self._skills[skill_id]

    def get_skills(
        self
    ) -> list[Skill]:

        return list(self._skills.values())