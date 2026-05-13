from __future__ import annotations

from typing import List
import numpy as np
import pandas as pd

import bentoml
from pydantic import BaseModel, Field, conint, confloat


# ======================
# Chargement du modele
# ======================

MODEL_TAG = "seattle_energy_model:nasblxaa4odyasqr"

bento_model_ref = bentoml.models.get(MODEL_TAG)
model = bentoml.sklearn.load_model(bento_model_ref)

CUSTOM = bento_model_ref.custom_objects or {}
TARGET_TRANSFORM = CUSTOM.get("target_transform", "none")


# ======================
# Schemas Pydantic
# ======================

class BuildingInput(BaseModel):
    PropertyGFATotal: confloat(gt=0) = Field(..., description="Total GFA")
    YearBuilt: conint(ge=1800, le=2100) = Field(..., description="Year built")
    NumberofFloors: conint(ge=1, le=200) = Field(..., description="Number of floors")
    PrimaryPropertyType: str = Field("Office", description="Primary property type")


class PredictRequest(BaseModel):
    items: List[BuildingInput] = Field(..., min_length=1)


class PredictResponse(BaseModel):
    # Fix warning Pydantic: conflit namespace "model_"
    model_config = {"protected_namespaces": ()}

    predictions_log: List[float]
    predictions_kbtu: List[float]
    model_tag: str


# ======================
# Feature engineering
# ======================

def build_feature_dataframe(items: List[BuildingInput]) -> pd.DataFrame:
    df = pd.DataFrame([i.model_dump() for i in items])

    # Features derivees (Mission 1)
    df["LogPropertyGFATotal"] = np.log1p(df["PropertyGFATotal"])
    df["GFA_per_Floor"] = df["PropertyGFATotal"] / df["NumberofFloors"]
    df["Age_x_GFA"] = (2025 - df["YearBuilt"]) * df["PropertyGFATotal"]

    # Colonnes requises par le pipeline
    defaults = {
        "Latitude": 47.60,
        "Longitude": -122.33,
        "Neighborhood": "UNKNOWN",
        "City": "Seattle",
        "State": "WA",
        "ZipCode": "00000",
        "CouncilDistrictCode": 0,
        "BuildingType": "NonResidential",
        "LargestPropertyUseType": df["PrimaryPropertyType"],
        "ListOfAllPropertyUseTypes": df["PrimaryPropertyType"],
        "NumberofBuildings": 1,
        "PropertyGFAParking": 0.0,
        "ENERGYSTARScore": 0,
        "GHGEmissionsIntensity": 0.0,
        "Electricity(kWh)": 0.0,
        "NaturalGas(therms)": 0.0,
        "SteamUse(kBtu)": 0.0,
        "ComplianceStatus": "Unknown",
        "DefaultData": False,
        "DataYear": 2020,
    }

    for col, value in defaults.items():
        df[col] = value

    return df


# ======================
# Service BentoML (nouveau style)
# ======================

@bentoml.service(name="seattle_energy_api")
class SeattleEnergyAPI:

    @bentoml.api
    def predict(self, req: PredictRequest) -> PredictResponse:
        X = build_feature_dataframe(req.items)

        pred_log = np.asarray(model.predict(X)).ravel().astype(float)

        if TARGET_TRANSFORM == "log1p":
            pred_kbtu = np.expm1(pred_log)
        else:
            pred_kbtu = pred_log

        return PredictResponse(
            predictions_log=pred_log.tolist(),
            predictions_kbtu=pred_kbtu.tolist(),
            model_tag=str(bento_model_ref.tag),
        )

