"""Inspecte la structure brute des records OpenDataSoft."""

from pathlib import Path
import json


RAW_FILE = Path("data/raw/events_raw.json")


def main() -> None:
    with RAW_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    records = data.get("records", [])

    print(f"Nombre de records : {len(records)}")

    if not records:
        print("Aucun record trouvé.")
        return

    first_record = records[0]
    fields = first_record.get("fields", {})

    print("\nClés du premier record :")
    print(list(first_record.keys()))

    print("\nClés du bloc 'fields' :")
    print(sorted(fields.keys()))

    print("\nChamps contenant 'date' ou 'time' :")
    date_keys = [key for key in fields.keys() if "date" in key.lower() or "time" in key.lower()]
    print(sorted(date_keys))

    print("\nValeurs des champs date/time du premier record :")
    for key in sorted(date_keys):
        print(f"{key}: {fields.get(key)}")


if __name__ == "__main__":
    main()