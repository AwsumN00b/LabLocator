import os
import sys
import uuid

import mysql.connector
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Annotated

from model import *

ip_address = sys.argv[1]
port = int(sys.argv[2])

knn_model = joblib.load("model/knn.joblib")

db_host = os.environ.get('SQLHOST')
db_user = os.environ.get('SQLUSER')
db_pass = os.environ.get('SQLPASS')
db_port = os.environ.get('SQLPORT')
db = os.environ.get('SQLDB')

description = """
# BusyLabs - Backend API
Returns McNulty lab location predictions 
"""

app = FastAPI(
    title="BusyLabs API",
    description=description
)

db_connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    port=db_port,
    database=db
)
db_cursor = db_connection.cursor()


class RoomData(BaseModel):
    device_id: str
    timestamp: int
    aplist: Annotated[list[str] | None, Query()] = None


@app.put('/room')
async def read_app_data(data: RoomData):
    if len(data.aplist) == 0 or data.aplist is None:
        raise HTTPException(status_code=406, detail="No Access Points provided")

    try:
        result = get_prediction(data.aplist)
    except IndexError:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    log_user_location(result, data.device_id, data.timestamp)

    return {"prediction": result[0]}


def get_prediction(ap_list):
    converted_scan = convert_scan(ap_list)
    return predict_single_scan(knn_model, converted_scan)


def log_user_location(room, device_id, time):
    sql = "INSERT into user_location_table (id, room, deviceID, time) VALUES (%s, %s, %s, %s)"
    val = (str(uuid.uuid4()), room, device_id, time)
    db_cursor.execute(sql, val)

    db_connection.commit()
    print(f"{time}: User {device_id} has been logged in {room}")


if __name__ == "__main__":
    uvicorn.run(app, host=ip_address, port=port)
