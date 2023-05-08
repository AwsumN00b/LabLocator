import os
import sys
from collections import defaultdict

import mysql.connector
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Annotated

from model import *

try:
    ip_address = sys.argv[1]
    port = int(sys.argv[2])
except IndexError:
    ip_address = "localhost"
    port = "8000"

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

    log_user_location(result[0], data.device_id)

    return {"prediction": result[0]}


# simple route to get the friends list and their current locations
@app.get('/friends')
async def get_friends_list():
    ping_db()
    # return friend names + current rooms
    sql = "SELECT user_name, current_room FROM user_table"
    db_cursor.execute(sql)

    return {i[0]: i[1] for i in db_cursor}


@app.get("/room/{room_id}")
async def get_room_data(room_id):
    if room_id == "quiet":
        room_data = room_population(get_all_devices_this_hour())
        if len(room_data) == 0:
            return "LG25", "0%"
        return least_populated_room(room_data)
    room_data = get_device_locations_in_room_this_hour(room_id)
    return room_population(room_data, room_id)


@app.get("/room/")
async def get_all_room_data():
    room_data = get_all_devices_this_hour()
    return room_population(room_data)


def get_prediction(ap_list):
    converted_scan = convert_scan(ap_list)
    return predict_single_scan(knn_model, converted_scan)


def log_user_location(room, device_id):
    ping_db()
    sql = "INSERT into user_location_table (room, deviceID) VALUES (%s, %s)"
    val = (room, device_id)
    db_cursor.execute(sql, val)

    db_connection.commit()


def get_device_locations_in_room_this_hour(room):
    ping_db()
    sql = """
    SELECT id, room, deviceID, time
FROM lablocator_db.user_location_table
WHERE `time` >= DATE_SUB(NOW(), INTERVAL 1 HOUR) AND room = %s
ORDER BY time
;
    """
    db_cursor.execute(sql, [room])

    result = db_cursor.fetchall()
    return result


def room_population(query_list, room=None):
    population = defaultdict(zero)
    seen = []
    for q in query_list:
        if q[2] not in seen:
            seen.append(q[2])
            population[q[1]] += 1

    if room:
        return {"population": population[room], "percent": population_percent(room, population[room])}

    total_population = {}
    for lab in population.keys():
        total_population[lab] = {"population": population[lab], "percent": population_percent(lab, population[lab])}
    return total_population


def population_percent(lab, number):
    lab_capacity = {
        "L125": 70,
        "L128": 60,
        "L129": 40,
        "LG25": 50,
        "LG26": 50,
        "LG27": 40,
        "L114": 59,
        "L101": 69
    }
    return str(round((number / lab_capacity[lab]) * 100)) + "%"


def get_all_devices_this_hour():
    ping_db()
    sql = """
    SELECT id, room, deviceID, time
FROM lablocator_db.user_location_table
WHERE `time` >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY time
;
    """
    db_cursor.execute(sql)

    result = db_cursor.fetchall()
    return result


def least_populated_room(lab_data):
    quiet_lab = "LG25"
    for lab in lab_data:
        if lab_data[lab]["population"] < lab_data[quiet_lab]["population"]:
            quiet_lab = lab

    return {"lab": quiet_lab, "stats": lab_data[quiet_lab]}


def ping_db():
    global db_connection
    db_connection.ping(True)


def zero():
    return 0


if __name__ == "__main__":
    uvicorn.run(app, host=ip_address, port=port)
