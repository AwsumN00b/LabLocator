from fastapi import FastAPI
from random import choice

busylabs_backend = FastAPI()

# read_root(data_from_app)
# location, time, ssid, bssid, rssi, ap list

@busylabs_backend.get("/")
def read_app_data(location: str, time: int, aplist: str):
    aplist = calculate_prediction(aplist.strip("{}").split())
    return {"result": aplist}


# emulation of prediction -- not yet integrated
def calculate_prediction(aplist):
    print("\n\npredicted!\n\n")
    p = ["lg25", "lg26", "lg27"]

    return choice(p)
