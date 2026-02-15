from typing import Any, Dict

import pandas as pd

from ml_prediction_web_service.entities.dictionary import (
    Site
)
from ml_prediction_web_service.entities.entities import (
    PerovskiteComposition,
    PCET80PredictionRequest,
    BandGapPredictionRequest,
    JVDefaultPCEPredictionRequest
)
from ml_prediction_web_service.services.features.calc_factors import compute_octahedral_factor, compute_tolerance_factor
from ml_prediction_web_service.services.features.structure_features import calculate_effective_radii


def _create_features_df(composition_entity: PerovskiteComposition) -> Dict[str, Any]:
    features = {
        "A_1": None, "A_2": None, "A_3": None,
        "A_1_coef": 0, "A_2_coef": 0, "A_3_coef": 0,
        "B_1": None, "B_2": None,
        "B_1_coef": 0, "B_2_coef": 0,
        "C_1": None, "C_2": None, "C_3": None,
        "C_1_coef": 0, "C_2_coef": 0, "C_3_coef": 0
    }

    def __fill_site(site_list, prefix, max_count):
        for i, element_fraction in enumerate(site_list[:max_count], start=1):
            features[f"{prefix}_{i}"] = element_fraction.name.nm
            features[f"{prefix}_{i}_coef"] = element_fraction.frequence

    __fill_site(composition_entity.A_site, Site.A.value, 3)
    __fill_site(composition_entity.B_site, Site.B.value, 2)
    __fill_site(composition_entity.C_site, Site.C.value, 3)

    # Pre-calculate effective radii and factors directly here
    r_A = calculate_effective_radii(composition_entity.A_site)
    r_B = calculate_effective_radii(composition_entity.B_site)
    r_C = calculate_effective_radii(composition_entity.C_site)

    features["r_A"] = r_A
    features["r_B"] = r_B
    features["r_C"] = r_C
    features["octahedral_factor"] = compute_octahedral_factor(r_B, r_C)
    features["tolerance_factor"] = compute_tolerance_factor(r_A, r_B, r_C)

    return features


def prepare_perovskites_composition_input(request: BandGapPredictionRequest) -> pd.DataFrame:
    composition_entity: PerovskiteComposition = request.perovskite_composition
    features = _create_features_df(composition_entity)
    df = pd.DataFrame([features])

    df["space_group"] = request.space_group.nm
    df["composition_inorganic"] = request.inorganic_composition
    df["dimension_list_of_layers"] = request.dimension_list_of_layers
    df["dimension"] = request.dimension.nm
    return df


def prepare_ts80_prediction_df(request: PCET80PredictionRequest) -> pd.DataFrame:
    composition_entity: PerovskiteComposition = request.perovskite_composition
    features = _create_features_df(composition_entity)
    df = pd.DataFrame([features])
    df["cell_architecture"] = request.cell_architecture.nm
    df["etl_stack_sequence"] = request.etl_stack_sequence.nm
    df["backcontact_stack_sequence"] = request.backcontact.nm
    df["stability_time_total_exposure"] = request.stability_time_total_exposure
    df["stability_light_intensity"] = request.stability_light_intensity
    df["stability_protocol"] = request.stability_protocol.nm
    df["PCE_initial"] = request.pce_initial
    df["cell_area_measured"] = request.cell_area
    df["encapsulation"] = False  # Defaulting to False as it's not in request
    df["band_gap"] = request.band_gap
    df["dimension_list_of_layers"] = request.dimension_list_of_layers
    df["stability_temperature_start"] = request.temperature_range.temperature_start
    df["stability_temperature_end"] = request.temperature_range.temperature_end
    return df


def prepare_jv_pce_prediction_df(request: JVDefaultPCEPredictionRequest) -> pd.DataFrame:
    composition_entity: PerovskiteComposition = request.perovskite_composition
    features = _create_features_df(composition_entity)
    df = pd.DataFrame([features])
    df["cell_architecture"] = request.cell_architecture.nm
    df["etl_stack_sequence"] = request.etl_stack_sequence.nm
    df["htl_stack_sequence"] = request.htl_stack_sequence.nm
    df["backcontact_stack_sequence"] = request.backcontact.nm
    df["cell_area_measured"] = request.cell_area
    df["band_gap"] = request.band_gap
    df["dimension_list_of_layers"] = request.dimension_list_of_layers
    return df
