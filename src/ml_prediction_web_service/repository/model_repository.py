import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import joblib
from xgboost import XGBRegressor

from ml_prediction_web_service.entities.model_dictionary import SavedModelName
from ml_prediction_web_service.google_storage.storage import GoogleDriveStorage


class ModelRepository(ABC):
    @staticmethod
    def _load_model(path: str | Path) -> Any:
        return joblib.load(path)

    @abstractmethod
    def get_band_gap_xgb_model(self):
        pass

    @abstractmethod
    def get_pce_t80_xgb_model(self):
        pass

    @staticmethod
    def _write_to_temp_file(model_bytes: bytes):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=True) as f:
            f.write(model_bytes)
            tmp_path = f.name
        return tmp_path


class GoogleModelRepository(ModelRepository):
    def __init__(
            self,
            google_drive: GoogleDriveStorage
    ):
        self._drive = google_drive

    def get_band_gap_xgb_model(self) -> XGBRegressor:
        pass

    def get_pce_t80_xgb_model(self) -> XGBRegressor:
        pass


class LocalModelRepository(ModelRepository):
    def __init__(
            self, models_path: str
    ):
        self._models_path = Path(models_path)

    def get_band_gap_xgb_model(self) -> XGBRegressor:
        path_to_model = self._models_path / SavedModelName.BAND_GAP_XGB.value
        return self._load_model(path_to_model)

    def get_pce_t80_xgb_model(self) -> XGBRegressor:
        path_to_model = self._models_path / SavedModelName.PCE_T80_XGB.value
        return self._load_model(path_to_model)
