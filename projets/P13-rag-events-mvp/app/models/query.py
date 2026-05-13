from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        description="Question ou recherche utilisateur"
    )

    top_k: int = Field(
        default=2,
        ge=1,
        le=10,
        description="Nombre de résultats à retourner"
    )