"""Nettoyage des événements OpenAgenda (format API) pour le projet RAG."""

from pathlib import Path
import json
import pandas as pd


RAW_FILE = Path("data/raw/events_raw.json")
OUTPUT_FILE = Path("data/processed/events_clean.csv")


def load_raw_data(path: Path) -> dict:
    """Charge le JSON brut."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_fr_text(value) -> str:
    """Extrait le texte français si la valeur est un dict multilingue."""
    if value is None:
        return ""

    if isinstance(value, dict):
        return str(value.get("fr") or value.get("en") or "").strip()

    return str(value).strip()


def normalize_keywords(value) -> str:
    """Normalise les mots-clés."""
    if value is None:
        return ""

    if isinstance(value, list):
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        return ", ".join(cleaned)

    return str(value).strip()


def extract_event_fields(event: dict) -> dict:
    """Extrait les champs utiles depuis un événement OpenAgenda API."""
    first_timing = event.get("firstTiming", {}) or {}
    last_timing = event.get("lastTiming", {}) or {}
    location = event.get("location", {}) or {}

    return {
        "uid": event.get("uid"),
        "title": get_fr_text(event.get("title")),
        "description": get_fr_text(event.get("description")),
        "longdescription": get_fr_text(event.get("longDescription")),
        "firstdate_begin": first_timing.get("begin"),
        "firstdate_end": first_timing.get("end"),
        "lastdate_begin": last_timing.get("begin"),
        "lastdate_end": last_timing.get("end"),
        "location_name": location.get("name", ""),
        "location_city": location.get("city", ""),
        "location_address": location.get("address", ""),
        "keywords_fr": normalize_keywords(event.get("keywords")),
        "access_link": event.get("canonicalUrl", ""),
        "attendance_mode": event.get("attendanceMode", ""),
        "status": event.get("status", ""),
    }


def clean_events(data: dict) -> pd.DataFrame:
    """Transforme les événements bruts en DataFrame nettoyé."""
    events = data.get("events", [])
    rows = [extract_event_fields(event) for event in events]

    df = pd.DataFrame(rows)

    print(f"Nombre de lignes brutes : {len(df)}")

    if df.empty:
        return df

    # Garde seulement les lignes utiles
    df = df.dropna(subset=["title", "firstdate_begin"]).copy()
    df = df[df["title"].astype(str).str.strip() != ""].copy()

    print(f"Après suppression des lignes sans titre/date : {len(df)}")

    # Description de secours
    df["description"] = df["description"].fillna("").astype(str).str.strip()
    df["longdescription"] = df["longdescription"].fillna("").astype(str).str.strip()
    df["description"] = df["description"].where(
        df["description"] != "",
        df["longdescription"]
    )

    # Nettoyage texte
    text_columns = [
        "title",
        "description",
        "location_name",
        "location_city",
        "location_address",
        "keywords_fr",
        "access_link",
        "attendance_mode",
        "status",
    ]
    for col in text_columns:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # Conversion des dates
    df["firstdate_begin_dt"] = pd.to_datetime(df["firstdate_begin"], errors="coerce", utc=True)
    df["firstdate_end_dt"] = pd.to_datetime(df["firstdate_end"], errors="coerce", utc=True)

    print(f"Dates valides après conversion : {df['firstdate_begin_dt'].notna().sum()}")

    df = df.dropna(subset=["firstdate_begin_dt"]).copy()
    print(f"Après suppression des dates invalides : {len(df)}")

    # Filtre métier : événements actuels / à venir
    now_utc = pd.Timestamp.now(tz="UTC")
    df = df[df["firstdate_begin_dt"] >= now_utc - pd.Timedelta(days=365)].copy()

    print(f"Après filtre métier 12 derniers mois / à venir : {len(df)}")

    # Suppression des doublons simples
    df = df.drop_duplicates(subset=["title", "firstdate_begin"]).copy()
    print(f"Après suppression des doublons : {len(df)}")

    # Export lisible
    df["firstdate_begin"] = df["firstdate_begin_dt"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["firstdate_end"] = df["firstdate_end_dt"].dt.strftime("%Y-%m-%d %H:%M:%S")

    df = df.drop(columns=["firstdate_begin_dt", "firstdate_end_dt", "longdescription"])

    return df


def save_clean_data(df: pd.DataFrame, output_path: Path) -> None:
    """Sauvegarde les données nettoyées en CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")


def main() -> None:
    """Exécute le pipeline de nettoyage."""
    data = load_raw_data(RAW_FILE)
    df = clean_events(data)
    save_clean_data(df, OUTPUT_FILE)

    print("\nPré-processing terminé")
    print(f"Nombre de lignes nettoyées : {len(df)}")
    print(f"Colonnes : {list(df.columns)}")
    print(f"Fichier sauvegardé : {OUTPUT_FILE}")

    if not df.empty:
        print("\nAperçu :")
        print(df[["title", "firstdate_begin", "location_city"]].head(5).to_string(index=False))


if __name__ == "__main__":
    main()