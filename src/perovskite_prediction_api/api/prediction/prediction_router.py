from fastapi import APIRouter, Depends

from perovskite_prediction_api.api.components import AppComponents
from perovskite_prediction_api.api.configuration import build_components
from perovskite_prediction_api.entities.entities import BandGapPredictionRequest, PCET80PredictionRequest

from perovskite_prediction_api.api.prediction.prediction_service import (
    predict_band_gap_service, predict_pce_t80_service
)

router = APIRouter(prefix="/prediction", tags=["Prediction Model"])


@router.post("/band_gap")
def predict_band_gap(
        request: BandGapPredictionRequest,
        components: AppComponents = Depends(build_components)
):
    return predict_band_gap_service(request, components)


@router.post("/stability_pce_t80")
def predict_stability_pce_t80(
        request: PCET80PredictionRequest,
        components: AppComponents = Depends(build_components)
):
    return predict_pce_t80_service(request, components)


@router.post("/jv_default_pce")
def predict_jv_default_pce(
        components: AppComponents = Depends(build_components)
):
    ...
