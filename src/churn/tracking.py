import os

from sklearn.pipeline import Pipeline

EXPERIMENT = "mobil-churn"

MATT = ("roc_auc", "accuracy")


def logga_korningarna(modell: Pipeline, matvarden: dict, parametrar: dict) -> None:
    if not os.environ.get("MLFLOW_TRACKING_URI"):
        return

    import mlflow

    mlflow.set_experiment(EXPERIMENT)
    with mlflow.start_run():
        mlflow.log_params(parametrar)
        mlflow.log_metrics({k: v for k, v in matvarden.items() if k in MATT})
        mlflow.set_tags({k: str(v) for k, v in matvarden.items() if k not in MATT})
        mlflow.sklearn.log_model(
            modell, 
            name="modell", 
            skops_trusted_types=["numpy.dtype"]
        )