from dataclasses import dataclass

from perovskite_prediction_api.repository.model_repository import ModelRepository


@dataclass
class Env:
    MODELS_PATH: str


@dataclass
class AppComponents:
    model_repository: ModelRepository
    
