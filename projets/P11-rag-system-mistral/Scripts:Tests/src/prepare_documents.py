"""Prépare les documents texte qui seront vectorisés pour le système RAG."""

from pathlib import Path
import pandas as pd


INPUT_FILE = Path("data/processed/events_clean.csv")
OUTPUT_FILE = Path("data/processed/events_documents.csv")


def build_document(row: pd.Series) -> str:
    """Construit un texte unique par événement."""
    parts = [
        f"Titre : {row['title']}",
        f"Description : {row['description']}",
        f"Date de début : {row['firstdate_begin']}",
        f"Date de fin : {row['firstdate_end']}",
        f"Lieu : {row['location_name']}",
        f"Ville : {row['location_city']}",
        f"Adresse : {row['location_address']}",
        f"Mots-clés : {row['keywords_fr']}",
        f"Mode de participation : {row['attendance_mode']}",
        f"Statut : {row['status']}",
        f"Lien : {row['access_link']}",
    ]

    return "\n".join(part for part in parts if str(part).strip())


def main() -> None:
    """Lit les données nettoyées et prépare les documents texte."""
    df = pd.read_csv(INPUT_FILE)
    df = df.fillna("")

    if df.empty:
        print("Aucun document à préparer : events_clean.csv est vide.")
        return

    df["document"] = df.apply(build_document, axis=1)

    output_columns = [
        "uid",
        "title",
        "firstdate_begin",
        "location_city",
        "document",
    ]

    output_df = df[output_columns].copy()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print("Préparation des documents terminée")
    print(f"Nombre de documents : {len(output_df)}")
    print(f"Colonnes finales : {list(output_df.columns)}")
    print(f"Fichier sauvegardé : {OUTPUT_FILE}")
    print("\nAperçu du premier document :\n")
    print(output_df.iloc[0]["document"][:1000])


if __name__ == "__main__":
    main()