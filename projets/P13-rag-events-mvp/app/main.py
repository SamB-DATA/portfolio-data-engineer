from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.logger import get_logger
from app.core.settings import settings
from app.models.chat import ChatQuery
from app.models.query import SearchQuery
from app.services.chat_service import ChatService
from app.services.ingestion_service import IngestionService
from app.services.rag_service import RagService
from app.services.vector_store_service import VectorStoreService


logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API du système RAG événements culturels"
)

ingestion_service = IngestionService()
vector_store_service = VectorStoreService()
rag_service = RagService()
chat_service = ChatService()


@app.middleware("http")
async def log_requests(request: Request, call_next):

    logger.info(
        "Requête reçue - méthode=%s chemin=%s",
        request.method,
        request.url.path
    )

    response = await call_next(request)

    logger.info(
        "Réponse envoyée - méthode=%s chemin=%s status=%s",
        request.method,
        request.url.path,
        response.status_code
    )

    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    logger.exception(
        "Erreur non gérée - chemin=%s erreur=%s",
        request.url.path,
        str(exc)
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Erreur interne du serveur",
            "detail": str(exc)
        }
    )


@app.get("/")
def home():

    logger.info("Endpoint home appelé")

    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "message": "Bienvenue sur le MVP RAG Events"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.get("/config")
def get_config():

    return {
        "llm_model": settings.llm_model,
        "vector_store": settings.vector_store_path
    }


@app.get("/documents")
def get_documents():

    documents = ingestion_service.load_documents()

    return {
        "count": len(documents),
        "documents": documents
    }


@app.post("/rag/build-index")
def build_rag_index():

    logger.info("Construction de l'index FAISS demandée")

    return vector_store_service.build_index()


@app.get("/rag/status")
def rag_status():

    return vector_store_service.get_status()


@app.post("/rag/search")
def search_events(search_query: SearchQuery):

    logger.info("Recherche RAG - query=%s", search_query.query)

    return vector_store_service.search(
        query=search_query.query,
        top_k=search_query.top_k
    )


@app.post("/rag/answer")
def rag_answer(search_query: SearchQuery):

    logger.info("Réponse RAG - query=%s", search_query.query)

    return rag_service.answer_query(
        query=search_query.query,
        top_k=search_query.top_k
    )


@app.post("/rag/ask")
def rag_ask(search_query: SearchQuery):

    logger.info("Question RAG avec LLM - query=%s", search_query.query)

    return rag_service.answer_query(
        query=search_query.query,
        top_k=search_query.top_k
    )


@app.post("/chat/ask")
def chat_ask(chat_query: ChatQuery):

    logger.info(
        "Question chat - session_id=%s query=%s",
        chat_query.session_id,
        chat_query.query
    )

    return chat_service.ask(
        session_id=chat_query.session_id,
        query=chat_query.query,
        top_k=chat_query.top_k
    )


@app.get("/chat/history/{session_id}")
def chat_history(session_id: str):

    logger.info("Consultation historique - session_id=%s", session_id)

    return chat_service.get_history(session_id)


@app.delete("/chat/history/{session_id}")
def clear_chat_history(session_id: str):

    logger.info("Suppression historique - session_id=%s", session_id)

    return chat_service.clear_history(session_id)