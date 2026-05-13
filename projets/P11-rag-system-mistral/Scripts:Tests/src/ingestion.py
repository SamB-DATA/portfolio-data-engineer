"""Ingestion des événements publics depuis OpenDataSoft."""

from pathlib import Path
import requests
import json

URL = "https://public.opendatasoft.com/api/records/1.0/search/"

PARAMS = {
    "dataset": "evenements-publics-openagenda",
    "rows": 100,
    "sort": "firstdate_begin",
}


def fetch_events() -> dict:
    """Récupère les événements depuis OpenDataSoft."""
    response = requests.get(URL, params=PARAMS, timeout=30)
    response.raise_for_status()
    return response.json()


def save_json(data: dict, path: Path):
    """Sauvegarde les données en JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    data = fetch_events()

    records = data.get("records", [])
    print(f"Nombre d'événements récupérés : {len(records)}")

    save_json(data, Path("data/raw/events_raw.json"))
    print("Fichier sauvegardé : data/raw/events_raw.json")


if __name__ == "__main__":
    main()