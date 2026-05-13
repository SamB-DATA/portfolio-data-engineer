"""Pipeline RAG simple avec FAISS + Mistral."""

import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI


VECTORSTORE_PATH = "data/vectorstore"


def load_vectorstore():
    """Charge le vector store FAISS."""
    embeddings = MistralAIEmbeddings()

    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def retrieve_context(vectorstore, query, k=3):
    """Récupère les documents les plus proches."""
    docs = vectorstore.similarity_search(query, k=k)
    return docs


def build_prompt(query, docs):
    """Construit le prompt avec le contexte récupéré."""
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
Tu es un assistant spécialisé dans la recommandation d'événements culturels.

Réponds uniquement à partir du contexte ci-dessous.
Si l'information n'est pas présente, dis clairement que tu ne sais pas.

Contexte :
{context}

Question :
{query}

Réponse :
"""
    return prompt


def generate_answer(prompt):
    """Génère une réponse avec Mistral."""
    llm = ChatMistralAI(model="mistral-small-latest", temperature=0)
    response = llm.invoke(prompt)
    return response.content


def main():
    """Teste le pipeline RAG sur une question."""
    load_dotenv()

    if not os.path.exists(VECTORSTORE_PATH):
        raise FileNotFoundError("Le vector store n'existe pas encore.")

    vectorstore = load_vectorstore()

    query = "Je cherche une conférence scientifique intéressante"
    docs = retrieve_context(vectorstore, query, k=3)

    print("=== DOCUMENTS RETROUVÉS ===\n")
    for i, doc in enumerate(docs, start=1):
        print(f"--- Document {i} ---")
        print(doc.page_content[:800])
        print()

    prompt = build_prompt(query, docs)
    answer = generate_answer(prompt)

    print("\n=== RÉPONSE FINALE ===\n")
    print(answer)


if __name__ == "__main__":
    main()