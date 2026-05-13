from pydantic import BaseModel


class EventDocument(BaseModel):
    id: str
    title: str
    description: str
    location: str | None = None
    date: str | None = None
    source: str | None = None