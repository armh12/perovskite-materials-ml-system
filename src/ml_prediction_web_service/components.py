from dataclasses import dataclass

from ml_prediction_web_service.repository.model_repository import ModelRepository


@dataclass
class Env:
    MODELS_PATH: str


@dataclass
class AppComponents:
    model_repository: ModelRepository
    
