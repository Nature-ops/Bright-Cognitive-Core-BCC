from app.models.framework import Framework
from app.services.base_engine import BaseEngine
from app.services.framework_loader import FrameworkLoader


class FrameworkEngine(BaseEngine[Framework]):

    def __init__(self):
        super().__init__(FrameworkLoader())

    def get_framework(
        self,
        framework_id: str
    ) -> Framework:

        return self.get(framework_id)

    def get_frameworks(
        self
    ) -> list[Framework]:

        return self.get_all()