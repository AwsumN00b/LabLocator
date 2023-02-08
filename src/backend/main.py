from typing import Union

from fastapi import FastAPI
from random import choice


busylabs_backend = FastAPI()


# read_root(data_from_app)
# location, time, ssid, bssid, rssi, ap list


# adjust?
@busylabs_backend.get("/")
def read_app_data(location: str, time: int, aplist: str):
    aplist = calculate_prediction(aplist.strip("{}").split())
    return {"result": aplist}




def calculate_prediction(aplist):
    print("\n\npredicted!\n\n")
    p = ["lg25", "lg26", "lg27"]

    return choice(p)

@busylabs_backend.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
