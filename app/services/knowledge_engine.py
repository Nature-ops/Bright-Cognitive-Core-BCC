from pathlib import Path
from typing import Optional
from app.models.framework import Framework
from app.models.milestone import Milestone
from app.services.framework_loader import FrameworkLoader


class KnowledgeEngine:
    def __init__(self):
        self._framework: Optional[Framework] = None

    def load_framework(self, path: str | Path) -> None:
        """Load and store a knowledge framework."""
        self._framework = FrameworkLoader.load(path)

    def get_framework(self) -> Framework:
        """Return the currently loaded framework."""
        self._ensure_framework_loaded()
        return self._framework  # type: ignore

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

    def _ensure_framework_loaded(self) -> None:
        """Raise an error if no framework has been loaded."""
        if self._framework is None:
            raise RuntimeError("No framework has been loaded.")