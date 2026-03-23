from __future__ import annotations

from typing import Dict, List


def risk_band(probability: float) -> str:
    if probability < 0.30:
        return "Low"
    if probability < 0.70:
        return "Medium"
    return "High"


def format_metrics(metrics: Dict[str, float]) -> str:
    lines = ["Model evaluation:"]
    for key, value in metrics.items():
        lines.append(f"- {key}: {value:.4f}")
    return "\n".join(lines)


def safe_int(value):
    return int(round(float(value)))


def safe_float(value):
    return float(value)
