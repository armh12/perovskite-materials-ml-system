import os

import pytest
from typing import List

from dotenv import load_dotenv

from ml_prediction_web_service.components import AppComponents
from ml_prediction_web_service.entities.dictionary import Element, SpaceGroup, Dimension
from ml_prediction_web_service.entities.entities import BandGapPredictionRequest, PerovskiteComposition, ElementFraction
from ml_prediction_web_service.repository.model_repository import LocalModelRepository

load_dotenv()

MODELS_PATH = os.environ.get("MODELS_PATH")
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
            B_site=[ElementFraction(name=Element.PB, frequence=0.5), ElementFraction(name=Element.FA, frequence=0.5)],
            C_site=[ElementFraction(name=Element.CL, frequence=1.5), ElementFraction(name=Element.I, frequence=1.5)],
        ),
        space_group=SpaceGroup.CUBIC,
        dimension_list_of_layers=3.0,
        inorganic_composition=True,
        dimension=Dimension.THREE_DIM
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

