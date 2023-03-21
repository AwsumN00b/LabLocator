import sys

import uvicorn
from fastapi import FastAPI, HTTPException

from model import *

ip_address = sys.argv[1]
port = int(sys.argv[2])

knn_model = joblib.load("model/knn.joblib")

description = """
# BusyLabs - Backend API
Returns McNulty lab location predictions 
"""

app = FastAPI(
    title="BusyLabs API",
    description=description
)


@app.get('/room')
async def read_app_data(ap_str: str):
    ap_list = ap_str.split("|")

    if len(ap_list) == 0 or ap_str is None:
        raise HTTPException(status_code=406, detail="No Access Points provided")

    result = get_prediction(ap_list)
    return {"prediction": result[0]}


def get_prediction(ap_list):
    converted_scan = convert_scan(ap_list)
    return predict_single_scan(knn_model, converted_scan)


if __name__ == "__main__":
    uvicorn.run(app, host=ip_address, port=port)
