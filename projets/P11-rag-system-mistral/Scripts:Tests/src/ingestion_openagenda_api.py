"""Collecte des événements OpenAgenda via l'API pour un agenda unique.

Ce script :
1. charge la clé API depuis .env
2. récupère les événements d'un agenda OpenAgenda
3. sauvegarde la réponse brute dans data/raw/events_raw.json
"""

from pathlib import Path
from dotenv import load_dotenv
import json
import os
import requests


load_dotenv()

API_KEY = os.getenv("OPENAGENDA_API_KEY")
BASE_URL = "https://api.openagenda.com/v2"
AGENDA_UID = 86184123  # Université Paris-Saclay
OUTPUT_FILE = Path("data/raw/events_raw.json")


def get_headers() -> dict:
    """Retourne les headers d'authentification.

    Returns:
        dict: en-têtes HTTP contenant la clé API.

    Raises:
        ValueError: si la clé API est absente.
    """
    if not API_KEY:
        raise ValueError("OPENAGENDA_API_KEY est absente du fichier .env")

    return {"key": API_KEY}


def fetch_events_for_agenda(agenda_uid: int, size: int = 100) -> dict:
    """Récupère les événements d'un agenda OpenAgenda.

    Args:
        agenda_uid (int): identifiant de l'agenda.
        size (int, optional): nombre maximum d'événements à récupérer.

    Returns:
        dict: réponse JSON brute de l'API.

    Raises:
        requests.HTTPError: si la requête HTTP échoue.
    """
    url = f"{BASE_URL}/agendas/{agenda_uid}/events"

    params = {
        "size": size,
        "relative[]": ["current", "upcoming"],
        "detailed": 1,
    }

    response = requests.get(
        url,
        headers=get_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    return response.json()


def save_json(payload: dict, output_path: Path) -> None:
    """Sauvegarde un JSON sur disque.

    Args:
        payload (dict): données JSON à sauvegarder.
        output_path (Path): chemin du fichier de sortie.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def main() -> None:
    """Exécute la collecte d'événements."""
    payload = fetch_events_for_agenda(agenda_uid=AGENDA_UID, size=100)
    events = payload.get("events", [])

    print(f"Nombre d'événements récupérés : {len(events)}")

    if events:
        first_event = events[0]
        first_title = first_event.get("title", {}).get("fr", "Sans titre")
        first_timing = first_event.get("firstTiming", {})
        first_begin = first_timing.get("begin", "Date inconnue")

        print("Aperçu du premier événement :")
        print(f"- Titre : {first_title}")
        print(f"- Date début : {first_begin}")

    save_json(payload, OUTPUT_FILE)
    print(f"Fichier sauvegardé : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()