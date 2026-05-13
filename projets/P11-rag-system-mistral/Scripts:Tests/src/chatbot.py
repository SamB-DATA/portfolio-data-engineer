"""Chatbot RAG simple en ligne de commande."""

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
    return vectorstore.similarity_search(query, k=k)


def build_prompt(query, docs):
    """Construit le prompt pour le LLM."""
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
Tu es un assistant spécialisé dans la recommandation d'événements culturels.

Règles :
- Réponds uniquement à partir du contexte fourni.
- Si l'information n'est pas présente, dis clairement que tu ne sais pas.
- Donne une réponse claire, structurée et utile.
- Quand c'est possible, propose le titre, la date, le lieu et la ville.

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
    """Lance le chatbot en ligne de commande."""
    load_dotenv()

    if not os.path.exists(VECTORSTORE_PATH):
        raise FileNotFoundError("Le vector store n'existe pas encore.")

    vectorstore = load_vectorstore()

    print("Chatbot RAG prêt.")
    print("Tape ta question ou 'quit' pour arrêter.\n")

    while True:
        query = input("Votre question : ").strip()

        if query.lower() in {"quit", "exit", "q"}:
            print("Fin du chatbot.")
            break

        if not query:
            print("Merci de saisir une question.\n")
            continue

        docs = retrieve_context(vectorstore, query, k=3)
        prompt = build_prompt(query, docs)
        answer = generate_answer(prompt)

        print("\nRéponse :")
        print(answer)
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()