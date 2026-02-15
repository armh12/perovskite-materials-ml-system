from typing import List
from pydantic import BaseModel, model_validator

from ml_prediction_web_service.entities.dictionary import (
    Element,
    SpaceGroup,
    BackContact,
    ETLStack,
    CellArchitecture,
    Dimension,
    StabilityProtocol,
    HTLStack
)


class ElementFraction(BaseModel):
    name: Element
    frequence: float


class PerovskiteComposition(BaseModel):
    A_site: List[ElementFraction]
    B_site: List[ElementFraction]
    C_site: List[ElementFraction]

    @model_validator(mode='after')
    def check_fractions(self):
        total_A = sum(item.frequence for item in self.A_site)
        if not (0.99 <= total_A <= 1.01):
            raise ValueError(f'Fractions of A site must sum to 1.0, got {total_A}')

        total_B = sum(item.frequence for item in self.B_site)
        if not (0.99 <= total_B <= 1.01):
            raise ValueError(f'Fractions of B site must sum to 1.0, got {total_B}')

        total_C = sum(item.frequence for item in self.C_site)
        if not (2.99 <= total_C <= 3.01):
            raise ValueError(f'Fractions of C site must sum to 3.0, got {total_C}')
        return self


class BandGapPredictionRequest(BaseModel):
    perovskite_composition: PerovskiteComposition
    inorganic_composition: bool
    dimension_list_of_layers: float
    dimension: Dimension
    space_group: SpaceGroup


class StabilityTemperatureRange(BaseModel):
    temperature_start: float
    temperature_end: float


class PCET80PredictionRequest(BaseModel):
    perovskite_composition: PerovskiteComposition
    temperature_range: StabilityTemperatureRange
    band_gap: float
    dimension_list_of_layers: int
    cell_area: float
    pce_initial: float
    stability_protocol: StabilityProtocol
    stability_light_intensity: float
    stability_time_total_exposure: float
    backcontact: BackContact
    etl_stack_sequence: ETLStack
    cell_architecture: CellArchitecture


class JVDefaultPCEPredictionRequest(BaseModel):
    perovskite_composition: PerovskiteComposition
    band_gap: float
    dimension_list_of_layers: int
    cell_area: float
    backcontact: BackContact
    etl_stack_sequence: ETLStack
    htl_stack_sequence: HTLStack
    cell_architecture: CellArchitecture
