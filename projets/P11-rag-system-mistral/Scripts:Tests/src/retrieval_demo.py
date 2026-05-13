import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings


VECTORSTORE_PATH = "data/vectorstore"


def load_vectorstore():
    load_dotenv()

    embeddings = MistralAIEmbeddings()

    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def test_query(vectorstore, query, k=3):
    print(f"\nRequête : {query}\n")

    results = vectorstore.similarity_search(query, k=k)

    for i, doc in enumerate(results, start=1):
        print(f"--- Résultat {i} ---")
        print(doc.page_content[:1000])
        print()


def main():
    if not os.path.exists(VECTORSTORE_PATH):
        raise FileNotFoundError("Le vector store n'existe pas encore.")

    vectorstore = load_vectorstore()

    test_query(vectorstore, "Je cherche une exposition artistique à Paris")
    test_query(vectorstore, "Je veux assister à une conférence scientifique")
    test_query(vectorstore, "Je cherche un concert ce soir")


if __name__ == "__main__":
    main()