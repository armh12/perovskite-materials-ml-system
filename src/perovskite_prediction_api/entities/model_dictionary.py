import enum


@enum.unique
class SavedModelName(enum.Enum):
    BAND_GAP_XGB = "xgboost_band_gap.joblib"
    PCE_T80_XGB = "pce_t80_model.joblib"
    PCE_JV_XGB = "pce_jv_model.joblib"
