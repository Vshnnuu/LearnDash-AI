from __future__ import annotations

import joblib
import pandas as pd

from configs.settings import CHURN_THRESHOLD, FEATURE_COLS, MODEL_PATH
from src.agent import generate_retention_plan
from src.crm_simulator import simulate_crm_actions
from src.utils import risk_band


def load_model(path=MODEL_PATH):
    return joblib.load(path)


def predict_one(model, payload: dict) -> dict:
    row = {col: payload[col] for col in FEATURE_COLS}
    df = pd.DataFrame([row])

    probability = float(model.predict_proba(df)[0, 1])
    prediction = int(probability >= CHURN_THRESHOLD)
    risk = risk_band(probability)

    retention_plan = generate_retention_plan(payload, probability, risk)
    crm_actions = simulate_crm_actions(retention_plan["recommended_actions"])

    return {
        "churn_probability": probability,
        "prediction": prediction,
        "risk_level": risk,
        "churn_drivers": retention_plan["churn_drivers"],
        "recommended_actions": retention_plan["recommended_actions"],
        "execution_plan": retention_plan["execution_plan"],
        "crm_actions": crm_actions,
    }