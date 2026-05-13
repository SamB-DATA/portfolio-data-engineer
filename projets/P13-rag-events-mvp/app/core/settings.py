import os
from pathlib import Path

import yaml
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:

    def __init__(self):

        config_path = BASE_DIR / "config" / "app.yaml"

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

    @property
    def app_name(self):
        return self.config["application"]["name"]

    @property
    def app_version(self):
        return self.config["application"]["version"]

    @property
    def environment(self):
        return self.config["application"]["environment"]

    @property
    def llm_model(self):
        return os.getenv(
            "MISTRAL_MODEL",
            self.config["llm"]["model"]
        )

    @property
    def mistral_api_key(self):
        return os.getenv("MISTRAL_API_KEY")

    @property
    def vector_store_path(self):
        return os.getenv(
            "VECTOR_DB_PATH",
            self.config["vector_store"]["path"]
        )


settings = Settings()