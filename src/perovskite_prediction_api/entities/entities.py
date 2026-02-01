from typing import List
from pydantic import BaseModel, field_validator

from perovskite_prediction_api.entities.dictioanary_materials import ETLStack, CellArchitecture
from perovskite_prediction_api.entities.dictionary_api import Element, SpaceGroup, BackContact


class ElementFraction(BaseModel):
    name: Element
    frequence: float


class PerovskiteComposition(BaseModel):
    A_site: List[ElementFraction]
    B_site: List[ElementFraction]
    C_site: List[ElementFraction]


class BandGapPredictionRequest(BaseModel):
    inorganic_composition: bool
    perovskite_composition: PerovskiteComposition
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

