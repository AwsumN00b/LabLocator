from random import choice

import uvicorn
import sys
from fastapi import FastAPI, HTTPException

ip_address = sys.argv[1]
port = int(sys.argv[2])

description = """
# BusyLabs - Backend API
Returns McNulty lab location predictions 
"""

app = FastAPI(
    title="BusyLabs API",
    description=description
)


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
