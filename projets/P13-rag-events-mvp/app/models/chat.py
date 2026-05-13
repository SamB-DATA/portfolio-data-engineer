from pydantic import BaseModel, Field


class ChatQuery(BaseModel):
    session_id: str = Field(
        ...,
        min_length=3,
        description="Identifiant unique de session utilisateur"
    )

    query: str = Field(
        ...,
        min_length=3,
        description="Message utilisateur"
    )

    top_k: int = Field(
        default=2,
        ge=1,
        le=10,
        description="Nombre de documents à récupérer"
    )