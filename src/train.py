from __future__ import annotations

import json

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from configs.settings import MODEL_PATH, RANDOM_STATE, TEST_SIZE
from src.data_utils import get_X_y, load_dataset, validate_dataset
from src.features import build_preprocessor
from src.utils import format_metrics


def build_model_pipeline(model) -> Pipeline:
    preprocessor = build_preprocessor()
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )
    return pipeline


def evaluate_model(pipeline, X_train, X_test, y_train, y_test) -> dict:
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    probs = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1": f1_score(y_test, preds),
        "roc_auc": roc_auc_score(y_test, probs),
    }
    return metrics


def main():
    df = load_dataset()
    validate_dataset(df)
    X, y = get_X_y(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    negative_count = (y_train == 0).sum()
    positive_count = (y_train == 1).sum()
    scale_pos_weight = negative_count / positive_count

    models = {
        "logistic_regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            min_samples_split=8,
            min_samples_leaf=4,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            class_weight="balanced_subsample",
        ),
        "xgboost": XGBClassifier(
            n_estimators=600,
            learning_rate=0.03,
            max_depth=5,
            min_child_weight=3,
            subsample=0.8,
            colsample_bytree=0.8,
            gamma=1,
            reg_alpha=0.1,
            reg_lambda=1.0,
            scale_pos_weight=scale_pos_weight,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
    }

    results = {}
    trained_pipelines = {}

    for model_name, model in models.items():
        pipeline = build_model_pipeline(model)
        metrics = evaluate_model(pipeline, X_train, X_test, y_train, y_test)

        results[model_name] = metrics
        trained_pipelines[model_name] = pipeline

        print(f"\nModel: {model_name}")
        print(format_metrics(metrics))

    best_model_name = max(results, key=lambda name: results[name]["roc_auc"])
    best_pipeline = trained_pipelines[best_model_name]

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_pipeline, MODEL_PATH)

    metrics_path = MODEL_PATH.parent / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(
            {
                "best_model": best_model_name,
                "results": results,
            },
            f,
            indent=2,
        )

    print(f"\nBest model selected: {best_model_name}")
    print(f"Saved trained model to: {MODEL_PATH}")
    print(f"Saved metrics to: {metrics_path}")


if __name__ == "__main__":
    main()