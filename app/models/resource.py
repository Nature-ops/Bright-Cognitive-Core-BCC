from pydantic import BaseModel


class Resource(BaseModel):
    id: str
    title: str
    type: str
    url: str