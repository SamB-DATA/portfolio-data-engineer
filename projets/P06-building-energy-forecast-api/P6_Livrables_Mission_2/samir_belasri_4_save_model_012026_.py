import bentoml
import joblib
from pathlib import Path

MODEL_PATH = "artifacts/best_model_pipeline.joblib"

def main():
    model = joblib.load(MODEL_PATH)

    saved = bentoml.sklearn.save_model(
        name="seattle_energy_model",
        model=model,
        custom_objects={
            "target_transform": "log1p",
            "schema_version": 1,
        },
        metadata={
            "task": "regression",
            "target": "SiteEnergyUse(kBtu)",
        },
    )

    print(f"MODEL_TAG={saved.tag}")
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/model_tag.txt").write_text(str(saved.tag), encoding="utf-8")

if __name__ == "__main__":
    main()

