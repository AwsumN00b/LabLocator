import os
import sys
from errno import errorcode
from unittest import TestCase
from unittest.mock import patch

import mysql
import mysql.connector
import pytest
import utils
from fastapi.testclient import TestClient
from mock import patch

from main import app

client = TestClient(app)

sys_args = ["localhost", "8000"]


class MockDB(TestCase):
    @classmethod
    def setUpClass(cls):
        MYSQL_DB = os.environ.get('SQLDB')
        cnx = mysql.connector.connect(
            host=os.environ.get('SQLHOST'),
            user=os.environ.get('SQLUSER'),
            password=os.environ.get('SQLPASS'),
            port=os.environ.get('SQLPORT'),
        )
        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cursor.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            print("{}{}".format(MYSQL_DB, err))

        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_DB)
            )
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cnx.database = MYSQL_DB

        query = """
            CREATE TABLE `test_table` (
            `id` varchar(30) NOT NULL PRIMARY KEY ,
            `room` varchar(255) NOT NULL,
            `deviceID` varchar(255) NOT NULL,
            `time` timestamp NOT NULL
            )
            """
        try:
            cursor.execute(query)
            cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("test_table already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        # Insert data
        insert_data_query = """
        INSERT INTO `test_table` (`id`, `room`, `deviceID`, `time` VALUES
        (`1`, `LG25`, `test_id`, `21 December 2000 12:00:00`)
        (`2`, `LG22`, `android`, `1 April 2023 12:00:00`)
        """

        try:
            cursor.execute(insert_data_query)
            cnx.commit()
        except mysql.connector.Error as err:
            print("Data insertion to test_table failed \n" + err.msg)
        cursor.close()
        cnx.close()

        test_config = {
            "host": os.environ.get('SQLHOST'),
            "user": os.environ.get('SQLUSER'),
            "password": os.environ.get('SQLPASS'),
            "port": os.environ.get('SQLPORT'),
            "database": os.environ.get('SQLDB')
        }
        cls.mock_db_config = patch.dict(utils.config, test_config)

    @classmethod
    def tearDownClass(cls):
        cnx = mysql.connector.connect(
            host=os.environ.get('SQLHOST'),
            user=os.environ.get('SQLUSER'),
            password=os.environ.get('SQLPASS'),
            port=os.environ.get('SQLPORT'),
        )
        cursor = cnx.cursor(dictionary=True)

        # drop DB
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database {} does not exist. Dropping DB failed".format(MYSQL_DB))
        cnx.close()

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

    def test_read_app_data():
        global sys_args
        with patch.object(sys, "argv", sys_args):
            response = client.put("/room", json=fake_room_data)
            assert response.status_code == 200
            assert response.json() == {"prediction": "LG26"}

    if __name__ == '__main__':
        testing = pytest.main()
