import pytest
import pandas as pd
from ml_prediction_web_service.services.preparation import prepare_perovskites_composition_input
from tests.conftest import BAND_GAP_PREDICTION_REQUESTS


@pytest.mark.parametrize(
    "request_entity", BAND_GAP_PREDICTION_REQUESTS
)
def test_prepare_perovskites_composition_input(request_entity):
    df_input = prepare_perovskites_composition_input(request_entity)

    assert isinstance(df_input, pd.DataFrame)
    desired_columns_names = ["A_1", "A_2", "A_3", "B_1", "B_2", "C_1", "C_2", "C_3"]
    desired_columns_coefs = [f'{col}_coef' for col in desired_columns_names]
    desired_columns_struct = ["space_group", "composition_inorganic"]
    desired_columns = set(desired_columns_names + desired_columns_coefs + desired_columns_struct)
    assert len(desired_columns.difference(set(df_input.columns))) == 0