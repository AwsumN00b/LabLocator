from random import choice
import mysql.connector
import uvicorn
import sys
import os
from fastapi import FastAPI, HTTPException

ip_address = sys.argv[1]
port = int(sys.argv[2])

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


@app.get('/send')
async def send_app_data(room: str, deviceID: str, time: int):
    sql = "INSERT INTO user_location_table (room, deviceID, time) VALUES (%s, %s, %s)"
    val = (room, deviceID, time)
    db_cursor.execute(sql, val)

    db_connection.commit()

    return {"room": room, "time": time, "deviceID": deviceID}


@app.get('/room')
async def read_app_data(ap_str: str):
    ap_list = ap_str.split("|")

    if len(ap_list) == 0 or ap_str is None:
        raise HTTPException(status_code=406, detail="No Access Points provided")

    result = emulate_prediction(ap_list)
    return {"result": result}


# emulation of prediction -- to be further developed
# TODO: Move this to its own file
def emulate_prediction(ap_list):
    p = ["LG25", "LG26", "LG27", "L114", "L101"]

    return choice(p)


if __name__ == "__main__":
    uvicorn.run(app, host=ip_address, port=port)
