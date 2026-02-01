import pandas as pd

from perovskite_prediction_api.entities.dictioanary_materials import (
    Element, Site
)
from perovskite_prediction_api.entities.entities import (
    PerovskiteComposition,
    PCET80PredictionRequest,
)


def prepare_perovskites_composition_input(composition_entity: PerovskiteComposition) -> pd.DataFrame:
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
            features[f"{prefix}_{i}"] = element_fraction.name.value
            features[f"{prefix}_{i}_coef"] = element_fraction.frequence

    __fill_site(composition_entity.A_site, Site.A.value, 3)
    __fill_site(composition_entity.B_site, Site.B.value, 2)
    __fill_site(composition_entity.C_site, Site.C.value, 3)

    for k, v in features.items():
        if v is None:
            features[k] = 0.

    df = pd.DataFrame([features])
    return df


def prepare_ts80_prediction_df(request: PCET80PredictionRequest) -> pd.DataFrame:
    pass
