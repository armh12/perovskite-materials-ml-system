import os
import tempfile
from abc import ABC, abstractmethod

from xgboost import XGBRegressor

from perovskite_prediction_api.entities.model_dictionary import SavedModelName
from perovskite_prediction_api.google_storage.storage import GoogleDriveStorage


class ModelRepository(ABC):
    @abstractmethod
    def get_band_gap_xgb_model(self):
        pass

    @abstractmethod
    def get_pce_t80_xgb_model(self):
        pass

    def get_cell_architecture_model(self):
        pass

    def get_jv_pce_model(self):
        pass

    def get_thickness_model(self):
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
        model_bytes = self._drive.download_file(f"perovskite/models/{SavedModelName.BAND_GAP_XGB.value}")
        tmp_path = self._write_to_temp_file(model_bytes)
        model = XGBRegressor()
        model.load_model(tmp_path)
        return model
    
    
class LocalModelRepository(ModelRepository):
    def __init__(
        self, models_path: str
    ):
        self._models_path = models_path
        
    def get_band_gap_xgb_model(self) -> XGBRegressor:
        path_to_model = os.path.join(self._models_path, SavedModelName.BAND_GAP_XGB.value)
        model = XGBRegressor()
        model.load_model(path_to_model)
        return model

    def get_pce_t80_xgb_model(self) -> XGBRegressor:
        path_to_model = os.path.join(self._models_path, SavedModelName.PCE_T80_XGB.value)
        model = XGBRegressor()
        model.load_model(path_to_model)
        return model
