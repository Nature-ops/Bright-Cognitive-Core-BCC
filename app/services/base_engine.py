from pathlib import Path
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseEngine(Generic[T]):

    def __init__(self, loader):

        self.loader = loader
        self._items: dict[str, T] = {}

    def load_directory(
        self,
        directory: str | Path
    ) -> None:

        self._items.clear()

        directory = Path(directory)

        for file in directory.glob("*.yaml"):

            item = self.loader.load(file)


            if item.id in self._items:
                raise ValueError(
                    f"Duplicate ID '{item.id}' found in {file}"
                )

            self._items[item.id] = item




    def get(
        self,
        item_id: str
    ) -> T:

        return self._items[item_id]

    def get_all(
        self,
    ) -> list[T]:

        return list(self._items.values())