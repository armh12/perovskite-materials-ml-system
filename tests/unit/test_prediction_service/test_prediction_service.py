import pytest
from unittest.mock import MagicMock
from ml_prediction_web_service.services.prediction_service import (
    predict_band_gap_service,
    predict_pce_t80_service,
    predict_jv_default_pce_service
)
from tests.conftest import (
    BAND_GAP_PREDICTION_REQUESTS,
    PCE_T80_PREDICTION_REQUESTS,
    JV_PCE_PREDICTION_REQUESTS
)


@pytest.mark.parametrize("request_entity", BAND_GAP_PREDICTION_REQUESTS)
def test_predict_band_gap_service(request_entity, test_components):
    # Mock the model repository and the model itself
    mock_model = MagicMock()
    mock_model.predict.return_value = [1.55]  # Mock prediction result
    
    test_components.model_repository.get_band_gap_xgb_model = MagicMock(return_value=mock_model)
    
    result = predict_band_gap_service(request_entity, test_components)
    
    assert isinstance(result, dict)
    assert "band_gap" in result
    assert result["band_gap"] == 1.55
    test_components.model_repository.get_band_gap_xgb_model.assert_called_once()
    mock_model.predict.assert_called_once()


@pytest.mark.parametrize("request_entity", PCE_T80_PREDICTION_REQUESTS)
def test_predict_pce_t80_service(request_entity, test_components):
    # Mock the model repository and the model itself
    mock_model = MagicMock()
    mock_model.predict.return_value = [18.5]  # Mock prediction result
    
    test_components.model_repository.get_pce_t80_xgb_model = MagicMock(return_value=mock_model)
    
    result = predict_pce_t80_service(request_entity, test_components)
    
    assert isinstance(result, dict)
    assert "pce_t80" in result
    assert result["pce_t80"] == 18.5
    test_components.model_repository.get_pce_t80_xgb_model.assert_called_once()
    mock_model.predict.assert_called_once()


@pytest.mark.parametrize("request_entity", JV_PCE_PREDICTION_REQUESTS)
def test_predict_jv_default_pce_service(request_entity, test_components):
    # Mock the model repository and the model itself
    mock_model = MagicMock()
    mock_model.predict.return_value = [21.2]  # Mock prediction result
    
    test_components.model_repository.get_jv_pce_model = MagicMock(return_value=mock_model)
    
    result = predict_jv_default_pce_service(request_entity, test_components)
    
    assert isinstance(result, dict)
    assert "jv_default_pce" in result
    assert result["jv_default_pce"] == 21.2
    test_components.model_repository.get_jv_pce_model.assert_called_once()
    mock_model.predict.assert_called_once()
