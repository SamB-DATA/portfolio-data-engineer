import os
import pandas as pd
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings


def load_data():
    path = "data/processed/events_documents.csv"

    if not os.path.exists(path):
        raise FileNotFoundError("Fichier introuvable : events_documents.csv")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Le fichier est vide")

    return df


def build_vectorstore(df):
    texts = df["document"].tolist()

    print(f"Nombre de documents à vectoriser : {len(texts)}")

    embeddings = MistralAIEmbeddings()

    vectorstore = FAISS.from_texts(texts, embeddings)

    return vectorstore


def save_vectorstore(vectorstore):
    path = "data/vectorstore"

    vectorstore.save_local(path)

    print(f"Vector store sauvegardé dans : {path}")


def main():
    load_dotenv()

    df = load_data()
    vectorstore = build_vectorstore(df)
    save_vectorstore(vectorstore)


if __name__ == "__main__":
    main()