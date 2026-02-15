from typing import Dict

from ml_prediction_web_service.components import AppComponents
from ml_prediction_web_service.services.preparation import (
    prepare_perovskites_composition_input,
    prepare_ts80_prediction_df,
    prepare_jv_pce_prediction_df
)
from ml_prediction_web_service.entities.entities import (
    BandGapPredictionRequest,
    PCET80PredictionRequest,
    JVDefaultPCEPredictionRequest
)


def predict_band_gap_service(
        request: BandGapPredictionRequest,
        components: AppComponents
) -> Dict[str, float]:
    df_input = prepare_perovskites_composition_input(request)
    
    # Select columns required by the model
    df_input = df_input[
        ["composition_inorganic", "A_1", "A_2", "A_3", "A_1_coef", "A_2_coef", "A_3_coef", "B_1", "B_2", "B_1_coef",
         "B_2_coef", "C_1", "C_2", "C_3", "C_1_coef", "C_2_coef", "C_3_coef", "r_A", "r_B", "r_C", "octahedral_factor",
         "tolerance_factor", "space_group", "dimension_list_of_layers", "dimension"]
    ]
    
    model = components.model_repository.get_band_gap_xgb_model()
    prediction = model.predict(df_input)[0]
    return {"band_gap": float(prediction)}


def predict_pce_t80_service(
        request: PCET80PredictionRequest,
        components: AppComponents
) -> Dict[str, float]:
    df_input = prepare_ts80_prediction_df(request)
    
    # Select columns required by the PCE T80 model
    df_input = df_input[
        ["A_1", "A_2", "A_3", "A_1_coef", "A_2_coef", "A_3_coef", "B_1", "B_2", "B_1_coef", "B_2_coef", "C_1", "C_2",
         "C_3", "C_1_coef", "C_2_coef", "C_3_coef", "r_A", "r_B", "r_C", "octahedral_factor", "tolerance_factor",
         "cell_architecture", "etl_stack_sequence", "backcontact_stack_sequence", "stability_time_total_exposure",
         "stability_light_intensity", "stability_protocol", "PCE_initial", "cell_area_measured", "encapsulation",
         "band_gap", "dimension_list_of_layers", "stability_temperature_start", "stability_temperature_end"]
    ]
    model = components.model_repository.get_pce_t80_xgb_model()
    prediction = model.predict(df_input)[0]
    return {"pce_t80": float(prediction)}


def predict_jv_default_pce_service(
        request: JVDefaultPCEPredictionRequest,
        components: AppComponents
) -> Dict[str, float]:
    df_input = prepare_jv_pce_prediction_df(request)
    
    # Select columns required by the JV PCE model
    df_input = df_input[
        ["A_1", "A_2", "A_3", "A_1_coef", "A_2_coef", "A_3_coef", "B_1", "B_2", "B_1_coef", "B_2_coef", "C_1", "C_2",
         "C_3", "C_1_coef", "C_2_coef", "C_3_coef", "r_A", "r_B", "r_C", "octahedral_factor", "tolerance_factor",
         "cell_architecture", "etl_stack_sequence", "htl_stack_sequence", "backcontact_stack_sequence",
         "cell_area_measured", "band_gap", "dimension_list_of_layers"]
    ]
    model = components.model_repository.get_jv_pce_model()
    prediction = model.predict(df_input)[0]
    return {"jv_default_pce": float(prediction)}
