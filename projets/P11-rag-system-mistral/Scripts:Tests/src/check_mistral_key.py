from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("MISTRAL_API_KEY")

if key:
    print("Clé Mistral détectée :", key[:6] + "...")
else:
    print("Aucune clé Mistral détectée.")