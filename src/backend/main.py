import os
import sys

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
    # TODO: Log device, time, and room in DB

    return {"prediction": result[0]}


# simple route to get the friends list and their current locations
@app.get('/friends')
async def get_friends_list():
    # return friend names + current rooms
    sql = "SELECT user_name, current_room FROM user_table"
    db_cursor.execute(sql)

    return {i[0]: i[1] for i in db_cursor}


def get_prediction(ap_list):
    converted_scan = convert_scan(ap_list)
    return predict_single_scan(knn_model, converted_scan)


if __name__ == "__main__":
    uvicorn.run(app, host=ip_address, port=port)
