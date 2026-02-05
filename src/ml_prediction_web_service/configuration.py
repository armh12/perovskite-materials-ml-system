import os
from functools import lru_cache

from ml_prediction_web_service.components import AppComponents
from ml_prediction_web_service.repository.model_repository import LocalModelRepository

MODELS_BASE_PATH = "/ml_models"


@lru_cache
def build_components() -> AppComponents:
    path = get_model_path()
    model_repository = LocalModelRepository(path)
    return AppComponents(
        model_repository=model_repository,
    )


def get_model_path() -> str:
    models_path = os.environ.get("MODELS_PATH", MODELS_BASE_PATH)
    if not os.path.isdir(models_path):
        raise NotADirectoryError(f"No directory in {models_path}")
    return os.path.abspath(models_path)
