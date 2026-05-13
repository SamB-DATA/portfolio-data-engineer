"""Évaluation simple du système RAG sur un jeu de questions/réponses."""

from pathlib import Path
import json
import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI


VECTORSTORE_PATH = "data/vectorstore"
TEST_FILE = Path("data/test/test_qa.json")
OUTPUT_FILE = Path("data/test/test_results.json")


def load_vectorstore():
    """Charge le vector store FAISS."""
    embeddings = MistralAIEmbeddings()

    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def load_test_questions(path: Path) -> list[dict]:
    """Charge le jeu de test."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_context(vectorstore, query, k=3):
    """Récupère les documents les plus proches."""
    return vectorstore.similarity_search(query, k=k)


def build_prompt(query, docs):
    """Construit le prompt RAG."""
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
Tu es un assistant spécialisé dans la recommandation d'événements culturels.

Règles :
- Réponds uniquement à partir du contexte fourni.
- Si l'information n'est pas présente, dis clairement que tu ne sais pas.
- Donne une réponse courte, claire et structurée.
- Quand c'est possible, indique le titre, la date, le lieu et la ville.

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


def save_results(results: list[dict], path: Path) -> None:
    """Sauvegarde les résultats en JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)


def main():
    """Exécute l'évaluation simple du RAG."""
    load_dotenv()

    if not os.path.exists(VECTORSTORE_PATH):
        raise FileNotFoundError("Le vector store n'existe pas encore.")

    vectorstore = load_vectorstore()
    test_cases = load_test_questions(TEST_FILE)

    results = []

    for case in test_cases:
        question = case["question"]
        docs = retrieve_context(vectorstore, question, k=3)
        prompt = build_prompt(question, docs)
        generated_answer = generate_answer(prompt)

        results.append({
            "id": case["id"],
            "question": question,
            "expected_answer": case["expected_answer"],
            "generated_answer": generated_answer
        })

        print(f"[OK] Question {case['id']} traitée")

    save_results(results, OUTPUT_FILE)
    print(f"\nRésultats sauvegardés dans : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()