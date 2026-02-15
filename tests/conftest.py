import os

import pytest
from typing import List

from dotenv import load_dotenv

from ml_prediction_web_service.components import AppComponents
from ml_prediction_web_service.entities.dictionary import (
    Element, SpaceGroup, Dimension, BackContact, ETLStack, CellArchitecture, StabilityProtocol, HTLStack
)
from ml_prediction_web_service.entities.entities import (
    BandGapPredictionRequest, PerovskiteComposition, ElementFraction,
    PCET80PredictionRequest, StabilityTemperatureRange, JVDefaultPCEPredictionRequest
)
from ml_prediction_web_service.repository.model_repository import LocalModelRepository

load_dotenv()

# Use the absolute path to the ml_models directory in the project
MODELS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../ml_models"))

BAND_GAP_PREDICTION_REQUESTS: List[BandGapPredictionRequest] = [
    BandGapPredictionRequest(
        perovskite_composition=PerovskiteComposition(
            A_site=[ElementFraction(name=Element.MA, frequence=1.0)],
            B_site=[ElementFraction(name=Element.PB, frequence=1.0)],
            C_site=[ElementFraction(name=Element.CL, frequence=3.0)],
        ),
        space_group=SpaceGroup.CUBIC,
        dimension_list_of_layers=3.0,
        inorganic_composition=True,
        dimension=Dimension.THREE_DIM
    ),

    BandGapPredictionRequest(
        perovskite_composition=PerovskiteComposition(
            A_site=[ElementFraction(name=Element.MA, frequence=0.5), ElementFraction(name=Element.FA, frequence=0.5)],
            B_site=[ElementFraction(name=Element.PB, frequence=1.0)],
            C_site=[ElementFraction(name=Element.CL, frequence=1.5), ElementFraction(name=Element.I, frequence=1.5)],
        ),
        space_group=SpaceGroup.CUBIC,
        dimension_list_of_layers=3.0,
        inorganic_composition=True,
        dimension=Dimension.THREE_DIM
    )
]

PCE_T80_PREDICTION_REQUESTS: List[PCET80PredictionRequest] = [
    PCET80PredictionRequest(
        perovskite_composition=PerovskiteComposition(
            A_site=[ElementFraction(name=Element.MA, frequence=1.0)],
            B_site=[ElementFraction(name=Element.PB, frequence=1.0)],
            C_site=[ElementFraction(name=Element.I, frequence=3.0)],
        ),
        temperature_range=StabilityTemperatureRange(temperature_start=25.0, temperature_end=85.0),
        band_gap=1.6,
        dimension_list_of_layers=3,
        cell_area=0.1,
        pce_initial=20.0,
        stability_protocol=StabilityProtocol.ISOS_D_1,
        stability_light_intensity=100.0,
        stability_time_total_exposure=1000.0,
        backcontact=BackContact.Au,
        etl_stack_sequence=ETLStack.TI_O2_c,
        cell_architecture=CellArchitecture.NIP
    )
]

JV_PCE_PREDICTION_REQUESTS: List[JVDefaultPCEPredictionRequest] = [
    JVDefaultPCEPredictionRequest(
        perovskite_composition=PerovskiteComposition(
            A_site=[ElementFraction(name=Element.FA, frequence=1.0)],
            B_site=[ElementFraction(name=Element.PB, frequence=1.0)],
            C_site=[ElementFraction(name=Element.I, frequence=3.0)],
        ),
        band_gap=1.5,
        dimension_list_of_layers=3,
        cell_area=0.1,
        backcontact=BackContact.Ag,
        etl_stack_sequence=ETLStack.SN_O2_np,
        htl_stack_sequence=HTLStack.SPIRO_MEOTAD,
        cell_architecture=CellArchitecture.NIP
    )
]


@pytest.fixture
def test_components() -> AppComponents:
    model_repository = LocalModelRepository(
        models_path=MODELS_PATH
    )
    return AppComponents(
        model_repository=model_repository,
    )
