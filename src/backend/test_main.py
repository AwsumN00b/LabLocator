import os

import mysql.connector
import pytest
from fastapi.testclient import TestClient

from main import app

global db_cursor
global db_connection

client = TestClient(app)

fake_room_data = """
{
    "device_id": "test",
    "timestamp": 5000,
    "aplist": [
        "DCU-Guest-WiFi;70:3a:0e:62:e0:40;-75",
        "eduroam;70:3a:0e:62:e0:41;-75",
        "DCU-Guest-WiFi;70:3a:0e:62:e0:50;-68",
        "eduroam;70:3a:0e:62:e0:51;-69",
        "eduroam;24:f2:7f:ac:d4:e1;-57",
        "DCU-Guest-WiFi;24:f2:7f:ac:d4:e0;-57",
        "eduroam;24:f2:7f:ac:d4:41;-48",
        "DCU-Guest-WiFi;24:f2:7f:ac:d4:f0;-63",
        "eduroam;24:f2:7f:ac:d4:f1;-63",
        "eduroam;20:a6:cd:8e:a0:d1;-80",
        "DCU-Guest-WiFi;20:a6:cd:8e:a0:d0;-80",
        "DCU-Guest-WiFi;24:f2:7f:ac:d7:60;-69",
        "eduroam;24:f2:7f:ac:d7:71;-70",
        "DCU-Guest-WiFi;24:f2:7f:ac:d7:70;-70",
        "eduroam;20:a6:cd:90:e0:51;-76",
        "eduroam;24:f2:7f:ac:d1:31;-74",
        "eduroam;70:3a:0e:62:d7:31;-60",
        "DCU-Guest-WiFi;70:3a:0e:62:d7:30;-60",
        "DCU-Guest-WiFi;24:f2:7f:ac:d1:30;-73",
        "DCU-Guest-WiFi;20:a6:cd:90:e0:50;-76",
        "eduroam;24:f2:7f:ac:d4:51;-45",
        "DCU-Guest-WiFi;24:f2:7f:ac:d4:50;-45"
    ]
}
"""


@pytest.fixture(scope="session", autouse=True)
def db_create_drop():
    db_host = os.environ.get('SQLHOST')
    db_user = os.environ.get('SQLUSER')
    db_pass = os.environ.get('SQLPASS')
    db_port = os.environ.get('SQLPORT')
    db = os.environ.get('SQLDB')

    global db_connection
    db_connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        port=db_port,
        database=db
    )
    global db_cursor
    db_cursor = db_connection.cursor()

    create_queries = [
        """
        CREATE TABLE IF NOT EXISTS user_location_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room VARCHAR(255) NOT NULL,
            deviceID VARCHAR(255) NOT NULL,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS rooms (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room VARCHAR(255)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS user_table (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_name char(20),
            current_room char(4)
        );
        """]

    for query in create_queries:
        db_cursor.execute(query)

    more = True
    while more is True:
        more = db_cursor.nextset()

    yield

    drop_query = "DROP TABLE IF EXISTS user_location_table, rooms, user_table;"
    db_cursor.execute(drop_query)
    db_cursor.close()


def test_get_all_room_data():
    response = client.get("/room/")
    assert response.status_code == 200


def test_read_app_data():
    response = client.put("/room", json={
        "device_id": "test",
        "timestamp": 5000,
        "aplist": [
            "DCU-Guest-WiFi;70:3a:0e:62:e0:40;-75",
            "eduroam;70:3a:0e:62:e0:41;-75",
            "DCU-Guest-WiFi;70:3a:0e:62:e0:50;-68",
            "eduroam;70:3a:0e:62:e0:51;-69",
            "eduroam;24:f2:7f:ac:d4:e1;-57",
            "DCU-Guest-WiFi;24:f2:7f:ac:d4:e0;-57",
            "eduroam;24:f2:7f:ac:d4:41;-48",
            "DCU-Guest-WiFi;24:f2:7f:ac:d4:f0;-63",
            "eduroam;24:f2:7f:ac:d4:f1;-63",
            "eduroam;20:a6:cd:8e:a0:d1;-80",
            "DCU-Guest-WiFi;20:a6:cd:8e:a0:d0;-80",
            "DCU-Guest-WiFi;24:f2:7f:ac:d7:60;-69",
            "eduroam;24:f2:7f:ac:d7:71;-70",
            "DCU-Guest-WiFi;24:f2:7f:ac:d7:70;-70",
            "eduroam;20:a6:cd:90:e0:51;-76",
            "eduroam;24:f2:7f:ac:d1:31;-74",
            "eduroam;70:3a:0e:62:d7:31;-60",
            "DCU-Guest-WiFi;70:3a:0e:62:d7:30;-60",
            "DCU-Guest-WiFi;24:f2:7f:ac:d1:30;-73",
            "DCU-Guest-WiFi;20:a6:cd:90:e0:50;-76",
            "eduroam;24:f2:7f:ac:d4:51;-45",
            "DCU-Guest-WiFi;24:f2:7f:ac:d4:50;-45"
        ]
    })
    assert response.status_code == 200
    assert response.json() == {"prediction": "LG26"}
