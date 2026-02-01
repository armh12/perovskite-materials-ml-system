from fastapi import FastAPI

from perovskite_prediction_api.api.prediction.prediction_router import router as predictions_router

app = FastAPI()
app.include_router(predictions_router)

