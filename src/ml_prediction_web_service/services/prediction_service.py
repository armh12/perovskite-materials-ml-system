from typing import Dict

import pandas as pd

from ml_prediction_web_service.components import AppComponents
from ml_prediction_web_service.services.preparation import (
    prepare_perovskites_composition_input,
    prepare_ts80_prediction_df
)
from ml_prediction_web_service.entities.dictionary import Site
from ml_prediction_web_service.entities.entities import BandGapPredictionRequest, PCET80PredictionRequest
from ml_prediction_web_service.services.features import structure_features
from ml_prediction_web_service.services.features.calc_factors import compute_octahedral_factor, compute_tolerance_factor

SITE_COLS = ["A_1", "A_2", "A_3", "B_1", "B_2", "C_1", "C_2", "C_3"]


def _calculate_base_perovskite_factors(df_input: pd.DataFrame) -> pd.DataFrame:
    for site in Site:
        df_input[f"r_{site.value}"] = df_input.apply(
            lambda row: structure_features.calculate_effective_radii_for_site(row, site), axis=1
        )
    if df_input[["r_A", "r_B", "r_C"]].isnull().any().any():
        raise ValueError("Could not compute effective radii")

    df_input["octahedral_factor"] = df_input.apply(
        lambda row: compute_octahedral_factor(
            row["r_B"], row["r_C"]
        ), axis=1
    )
    df_input["tolerance_factor"] = df_input.apply(
        lambda row: compute_tolerance_factor(
            row["r_A"], row["r_B"], row["r_C"]
        ), axis=1
    )
    return df_input


def predict_band_gap_service(
        request: BandGapPredictionRequest,
        components: AppComponents
) -> Dict[str, float]:
    df_input = prepare_perovskites_composition_input(request)
    df_input = _calculate_base_perovskite_factors(df_input)
    df_input = df_input[
        ["composition_inorganic", "A_1", "A_2", "A_3", "A_1_coef", "A_2_coef", "A_3_coef", "B_1", "B_2", "B_1_coef",
         "B_2_coef", "C_1", "C_2", "C_3", "C_1_coef", "C_2_coef", "C_3_coef", "r_A", "r_B", "r_C", "octahedral_factor",
         "tolerance_factor", "space_group", "dimension_list_of_layers", "dimension"]

    ]
    model = components.model_repository.get_band_gap_xgb_model()
    return model.predict(df_input)[0]


def predict_pce_t80_service(
        request: PCET80PredictionRequest,
        components: AppComponents
) -> Dict[str, float]:
    df_input = prepare_ts80_prediction_df(request)
    df_input = _calculate_base_perovskite_factors(df_input)
    df_input = df_input[
        []
    ]
    model = components.model_repository.get_pce_t80_xgb_model()
    return model.predict(df_input)[0]
