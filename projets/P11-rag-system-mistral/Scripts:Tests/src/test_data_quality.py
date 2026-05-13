"""Tests unitaires de qualité des données pour le projet RAG."""

from pathlib import Path
import pandas as pd


DATA_FILE = Path("data/processed/events_clean.csv")


def test_file_exists():
    """Vérifie que le fichier nettoyé existe."""
    assert DATA_FILE.exists(), "Le fichier events_clean.csv est introuvable."


def test_file_not_empty():
    """Vérifie que le fichier nettoyé n'est pas vide."""
    df = pd.read_csv(DATA_FILE)
    assert not df.empty, "Le fichier events_clean.csv est vide."


def test_required_columns():
    """Vérifie la présence des colonnes obligatoires."""
    df = pd.read_csv(DATA_FILE)

    expected_columns = {
        "uid",
        "title",
        "description",
        "firstdate_begin",
        "firstdate_end",
        "location_name",
        "location_city",
        "location_address",
        "keywords_fr",
        "access_link",
        "attendance_mode",
        "status",
    }

    assert expected_columns.issubset(df.columns), "Colonnes obligatoires manquantes."


def test_titles_not_empty():
    """Vérifie que tous les titres sont renseignés."""
    df = pd.read_csv(DATA_FILE)
    assert df["title"].notna().all(), "Des titres sont manquants."
    assert (df["title"].astype(str).str.strip() != "").all(), "Des titres sont vides."


def test_dates_are_recent_or_upcoming():
    """Vérifie que les événements sont récents ou à venir (moins d'un an)."""
    df = pd.read_csv(DATA_FILE)

    df["firstdate_begin"] = pd.to_datetime(df["firstdate_begin"], errors="coerce")
    assert df["firstdate_begin"].notna().all(), "Certaines dates sont invalides."

    now = pd.Timestamp.now()
    one_year_ago = now - pd.Timedelta(days=365)

    assert (df["firstdate_begin"] >= one_year_ago).all(), (
        "Certains événements sont plus anciens qu'un an."
    )


def test_selected_geographic_scope():
    """Vérifie que les événements restent dans le périmètre du dataset choisi."""
    df = pd.read_csv(DATA_FILE)

    allowed_cities = {
        "Évry",
        "Évry-Courcouronnes",
        "Paris",
        "Saclay",
        "Gif-sur-Yvette",
        "Palaiseau",
        "Saint-Aubin",
        "Orsay",
        "Versailles",
        "Bures-sur-Yvette",
        "Pantin",
        "Le Kremlin-Bicêtre",
        "Guyancourt",
    }

    actual_cities = set(df["location_city"].dropna().astype(str).str.strip().unique())

    assert actual_cities.issubset(allowed_cities), (
        f"Des villes hors périmètre ont été trouvées : {actual_cities - allowed_cities}"
    )