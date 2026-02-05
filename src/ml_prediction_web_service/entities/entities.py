from typing import List
from pydantic import BaseModel, Field, validator, field_validator

from ml_prediction_web_service.entities.dictionary import (
    Element,
    SpaceGroup,
    BackContact,
    ETLStack,
    CellArchitecture,
    Dimension
)


class ElementFraction(BaseModel):
    name: Element
    frequence: float


class PerovskiteComposition(BaseModel):
    A_site: List[ElementFraction]
    B_site: List[ElementFraction]
    C_site: List[ElementFraction]

    @field_validator('A_site', 'B_site', 'C_site')
    def check_fractions(cls, v):
        total = sum(item.frequence for item in v)
        if not (0.99 <= total <= 1.01):  # Allowing for minor float rounding
            raise ValueError(f'Fractions must sum to 1.0, got {total}')
        return v


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
    stability_protocol: str
    stability_light_intensity: float
    stability_time_total_exposure: float
    backcontact: BackContact
    etl_stack_sequence: ETLStack
    cell_architecture: CellArchitecture

