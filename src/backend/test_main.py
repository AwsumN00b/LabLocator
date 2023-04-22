import os
import sys
from unittest.mock import patch

import mysql
import mysql.connector
import pytest
from fastapi.testclient import TestClient
from mock import patch

from main import app

client = TestClient(app)

sys_args = ["localhost", "8000"]

MYSQL_DB = os.environ.get('SQLDB')


@pytest.fixture(scope="session")
def db():
    cnx = mysql.connector.connect(user='user', password='password',
                                  host='localhost', database='test_db')
    cursor = cnx.cursor()
    cursor.execute(
        """CREATE TABLE user_location_table (
        id INT AUTO_INCREMENT PRIMARY KEY, room VARCHAR(255), deviceID VARCHAR(255)), time TIMESTAMP"""
    )
    cnx.commit()
    yield cnx
    cursor.execute("DROP TABLE items")
    cnx.commit()
    cursor.close()
    cnx.close()


@pytest.fixture(scope="function")
def cursor(db):
    cnx = db
    cursor = cnx.cursor()
    yield cursor
    cnx.rollback()
    cursor.close()


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


def test_create_item(cursor):
    cursor.execute("INSERT INTO user_location_table (room, deviceID) VALUES (%s, %s)", ("Test Room", "Test ID"))
    assert cursor.lastrowid is not None


def test_get_item(cursor):
    cursor.execute("INSERT INTO user_location_table (room, deviceID) VALUES (%s, %s)", ("Test Room", "Test ID"))
    item_id = cursor.lastrowid
    cursor.execute("SELECT id, room, deviceID FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    assert item is not None
    assert item[0] == item_id
    assert item[1] == "Test Room"
    assert item[2] == "Test ID"


def test_read_app_data():
    global sys_args, fake_room_data
    with patch.object(sys, "argv", sys_args):
        response = client.put("/room", json=fake_room_data)
        assert response.status_code == 200
        assert response.json() == {"prediction": "LG26"}


if __name__ == '__main__':
    testing = pytest.main()
