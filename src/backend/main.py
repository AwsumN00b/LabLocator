from fastapi import FastAPI
from random import choice

busylabs_backend = FastAPI()


@busylabs_backend.get("/")
def read_app_data():
    aplist = emulate_prediction(aplist.strip("{}").split())
    return {"result": aplist}


# emulation of prediction -- to be further developed
def emulate_prediction(aplist):
    p = ["LG25", "LG26", "LG27", "L114", "L101"]

    return choice(p)
