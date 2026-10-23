"""Prediktions-API. Kör:  uvicorn churn.api:app --reload"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from churn.data import FEATURES, skapa_features

MODELLFIL = Path(os.environ.get("MODELLFIL", "outputs/modell.joblib"))
modell = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global modell
    if MODELLFIL.exists():
        modell = joblib.load(MODELLFIL)
    yield


app = FastAPI(title="Churn-API", lifespan=lifespan)


class Kund(BaseModel):
    alder: int = Field(ge=16, le=110)
    manader_som_kund: int = Field(ge=0)
    manadskostnad: float = Field(ge=0)
    data_gb_per_manad: float = Field(ge=0)
    supportarenden_12m: int = Field(ge=0)
    region: str
    abonnemang: str


@app.get("/health")
def health():
    return {"status": "ok", "modell_laddad": modell is not None}


@app.post("/predict")
def predict(kund: Kund):
    if modell is None:
        raise HTTPException(503, f"Ingen modell i {MODELLFIL}")
    X = skapa_features(pd.DataFrame([kund.model_dump()]))[FEATURES]
    return {"risk": round(float(modell.predict_proba(X)[0, 1]), 3)}
