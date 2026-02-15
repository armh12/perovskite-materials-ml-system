import pytest

from conftest import BAND_GAP_PREDICTION_REQUESTS
from ml_prediction_web_service.services.prediction_service import predict_band_gap_service


@pytest.mark.parametrize(
    "request_entity", BAND_GAP_PREDICTION_REQUESTS
)
def test_predict_band_gap_service(request_entity, test_components):
    band_gap = predict_band_gap_service(request_entity, test_components)
    assert isinstance(band_gap, float)
