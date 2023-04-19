import os
import sys
from collections import defaultdict

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

    log_user_location(result[0], data.device_id, data.timestamp)

    return {"prediction": result[0]}


@app.get("/room/{room_id}")
async def get_room_data(room_id):
    room_data = get_device_locations_in_room_this_hour(room_id)
    return room_population(room_data, room_id)


@app.get("/room/")
async def get_all_room_data():
    room_data = get_all_devices_this_hour()
    return room_population(room_data)


def get_prediction(ap_list):
    converted_scan = convert_scan(ap_list)
    return predict_single_scan(knn_model, converted_scan)


def log_user_location(room, device_id, time):
    sql = "INSERT into user_location_table (room, deviceID) VALUES (%s, %s)"
    val = (room, device_id)
    db_cursor.execute(sql, val)

    db_connection.commit()
    print(f"{time}: User {device_id} has been logged in {room}")


def get_device_locations_in_room_this_hour(room):
    sql = """
    select * from lablocator_db.user_location_table where
    `time` >= DATE_SUB(NOW(), INTERVAL 1 HOUR) and
    room = (%s)
    """
    db_cursor.execute(sql, [room])

    result = db_cursor.fetchall()
    return result


def room_population(query_list, room=None):
    population_dict = defaultdict(zero)

    for entry in query_list:
        population_dict[entry[1]] += 1

    if room is not None:
        return population_dict[room]
    return population_dict


def get_all_devices_this_hour():
    sql = """
    SELECT * FROM lablocator_db.user_location_table WHERE
    `time` >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
    """
    db_cursor.execute(sql)

    result = db_cursor.fetchall()
    return result


def zero():
    return 0


if __name__ == "__main__":
    uvicorn.run(app, host=ip_address, port=port)
