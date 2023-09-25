from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
import pandas as pd
from challenge import model

app = FastAPI()
delay_model = model.DelayModel()
data = pd.read_csv(filepath_or_buffer="data/data.csv")

@app.get("")
def index():
    response = RedirectResponse(url= '/docs')
    return response

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(flights: dict) -> dict:
    predictions = []

    for flight in flights.get("flights", []):  # Ensure you have a default value for "flights" key
        try:
            data_df = pd.DataFrame([flight])  # Convert the flight data to a DataFrame
            features = pd.concat([
                pd.get_dummies(data_df['OPERA'], prefix = 'OPERA'),
                pd.get_dummies(data_df['TIPOVUELO'], prefix = 'TIPOVUELO'), 
                pd.get_dummies(data_df['MES'], prefix = 'MES')], 
                axis = 1
            )
            preprocessed_data, preprocessed_target = delay_model.preprocess(data, "ALL")
            preprocessed_data = preprocessed_data[list(features)]
            delay_model.fit(preprocessed_data, preprocessed_target)
            prediction = delay_model.predict(features=features)  # Use the actual model for prediction
            predictions.extend(prediction)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")

    return {"predict": predictions}