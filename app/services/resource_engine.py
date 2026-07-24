from app.models.resource import Resource
from app.services.base_engine import BaseEngine
from app.services.resource_loader import ResourceLoader
from pathlib import Path


class ResourceEngine:

    def __init__(self):

        self._resources = {}

    def load_directory(self, directory):

        for file in Path(directory).glob("*.yaml"):

            resources = ResourceLoader.load(file)

            for resource in resources:

                if resource.id in self._resources:
                    raise ValueError(
                        f"Duplicate resource id: {resource.id}"
                    )

                self._resources[resource.id] = resource

    def get_resource(self, resource_id):

        return self._resources[resource_id]

    def get_resources(self):

        return list(self._resources.values())