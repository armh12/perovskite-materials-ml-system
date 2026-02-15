import pytest
import pandas as pd
from ml_prediction_web_service.services.preparation import (
    prepare_perovskites_composition_input,
    prepare_ts80_prediction_df,
    prepare_jv_pce_prediction_df
)
from tests.conftest import (
    BAND_GAP_PREDICTION_REQUESTS,
    PCE_T80_PREDICTION_REQUESTS,
    JV_PCE_PREDICTION_REQUESTS
)


@pytest.mark.parametrize(
    "request_entity", BAND_GAP_PREDICTION_REQUESTS
)
def test_prepare_perovskites_composition_input(request_entity):
    df_input = prepare_perovskites_composition_input(request_entity)

    assert isinstance(df_input, pd.DataFrame)
    desired_columns_names = ["A_1", "A_2", "A_3", "B_1", "B_2", "C_1", "C_2", "C_3"]
    desired_columns_coefs = [f'{col}_coef' for col in desired_columns_names]
    desired_columns_struct = ["space_group", "composition_inorganic", "r_A", "r_B", "r_C", "octahedral_factor", "tolerance_factor"]
    desired_columns = set(desired_columns_names + desired_columns_coefs + desired_columns_struct)
    
    assert len(desired_columns.difference(set(df_input.columns))) == 0
    assert not df_input["r_A"].isnull().any()
    assert not df_input["octahedral_factor"].isnull().any()


@pytest.mark.parametrize(
    "request_entity", PCE_T80_PREDICTION_REQUESTS
)
def test_prepare_ts80_prediction_df(request_entity):
    df_input = prepare_ts80_prediction_df(request_entity)

    assert isinstance(df_input, pd.DataFrame)
    # Check for specific columns required by PCE T80 model
    required_columns = [
        "cell_architecture", "etl_stack_sequence", "backcontact_stack_sequence",
        "stability_time_total_exposure", "stability_light_intensity", "stability_protocol",
        "PCE_initial", "cell_area_measured", "encapsulation", "band_gap",
        "dimension_list_of_layers", "stability_temperature_start", "stability_temperature_end",
        "r_A", "r_B", "r_C", "octahedral_factor", "tolerance_factor"
    ]
    
    for col in required_columns:
        assert col in df_input.columns
        
    assert df_input["stability_protocol"].iloc[0] == request_entity.stability_protocol.nm
    assert df_input["backcontact_stack_sequence"].iloc[0] == request_entity.backcontact.nm


@pytest.mark.parametrize(
    "request_entity", JV_PCE_PREDICTION_REQUESTS
)
def test_prepare_jv_pce_prediction_df(request_entity):
    df_input = prepare_jv_pce_prediction_df(request_entity)

    assert isinstance(df_input, pd.DataFrame)
    # Check for specific columns required by JV PCE model
    required_columns = [
        "cell_architecture", "etl_stack_sequence", "htl_stack_sequence", "backcontact_stack_sequence",
        "cell_area_measured", "band_gap", "dimension_list_of_layers",
        "r_A", "r_B", "r_C", "octahedral_factor", "tolerance_factor"
    ]
    
    for col in required_columns:
        assert col in df_input.columns

    assert df_input["htl_stack_sequence"].iloc[0] == request_entity.htl_stack_sequence.nm
