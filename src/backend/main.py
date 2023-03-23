import os
import sys

import mysql.connector
import uvicorn
from fastapi import FastAPI, HTTPException

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


@app.get('/send_location')
async def send_app_data(room: str, device_id: str, time: int):
    sql = "SELECT * FROM rooms"
    db_cursor.execute(sql)
    rooms = [i[1] for i in db_cursor]

    if room in rooms:
        sql = "INSERT INTO user_location_table (room, deviceID, time) VALUES (%s, %s, %s)"
        val = (room, device_id, time)

        db_cursor.execute(sql, val)
        db_connection.commit()

        return {"result": "200 OK"}

    return {"ERROR": "ROOM NOT FOUND"}


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
