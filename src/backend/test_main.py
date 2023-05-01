import os
import threading

import mysql.connector
import pytest
from fastapi.testclient import TestClient

from main import app

global db_cursor
global db_connection

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    terminator_thread = threading.Thread()
    terminator_thread.start()

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
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            user_name char(20),
            current_room char(4)
        );
        """]

    for query in create_queries:
        db_cursor.execute(query)

    db_connection.commit()

    yield

    print("DO WE EVER EVEN GET HERE?")

    terminator_thread.join()


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


@pytest.fixture(scope="function")
def generate_friends():
    query = "INSERT INTO user_table (user_name, current_room) VALUES ('John', 'LG26');"
    db_cursor.execute(query)
    db_connection.commit()

    yield

    query = "DELETE FROM user_table"
    db_cursor.execute(query)
    db_connection.commit()


def test_get_friends_list(generate_friends):
    response = client.get("/friends")

    assert response.status_code == 200
    assert response.json() == {"John": "LG26"}


@pytest.fixture(scope="function")
def generate_room_data():
    query = """
        INSERT INTO user_location_table(room, deviceID) VALUES
        ('LG25', 'android'),
        ('LG25', 'iphone'),
        ('LG25', 'nokia'),
        ('LG26', 'motorola'),
        ('LG26', 'nintendo3ds'),
        ('L114', 'oneplus'),
        ('L114', 'xiaomi'),
        ('L101', 'dcu-phone'),
        ('L101', 'trinity-spy'),
        ('L128', 'smart-fridge');
    """

    db_cursor.execute(query)
    db_connection.commit()

    yield

    query = "DELETE FROM user_location_table;"
    db_cursor.execute(query)
    db_connection.commit()


def test_get_room_data_quiet(mocker):
    mock_room_data = [
        (3, 'LG25'),
        (2, 'LG26'),
        (2, 'L114'),
        (2, 'L101'),
        (1, 'L128'),
    ]
    mocker.patch("main.get_all_devices_this_hour", return_value=mock_room_data)

    response = client.get("/room/quiet")

    assert response.status_code == 200
    assert response.json() == "L128"


def test_get_room_data(mocker):
    mock_device_locations_in_room = [
        (1, 'LG25'),
        (2, 'LG25'),
        (3, 'LG25'),
    ]
    mocker.patch("main.get_device_locations_in_room_this_hour", return_value=mock_device_locations_in_room)

    response = client.get("/room/LG25")

    assert response.status_code == 200
    assert response.json() == 3


def test_get_all_room_data(mocker):
    mock_room_population = {
        "LG25": 3,
        "LG26": 2,
        "L114": 2,
        "L101": 2,
        "L128": 1
    }
    mocker.patch("main.room_population", return_value=mock_room_population)

    response = client.get("room/")

    assert response.status_code == 200
    assert response.json() == mock_room_population
