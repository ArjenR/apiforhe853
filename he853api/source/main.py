import subprocess
import re

from typing import Optional
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/status")
def get_status():
    status = {}
    status.update({"exitcode": "9"})
    status.update({"result": "FAIL"})
    result = subprocess.run(["he853-static"], capture_output=True, text=True)
    print(result.stdout)
    status.update({"verbose_result": result.stdout })
    status.update({"exitcode": result.returncode })
    if (result.returncode == "0"):
        status.update({"result": "OK"})
    return status

@app.get("/help")
def get_help():
    status = {}
    result = subprocess.run(["he853-static", "--help"], capture_output=True, text=True)
    print(result.stdout)
    status.update({"verbose_result": result.stdout })
    status.update({"exitcode": result.returncode })
    if (result.returncode == "0"):
        status.update({"result": "OK"})
    return status

@app.get("/switch")
def action(action: str = Query(..., max_length=3, regex="^(on|off|\d{,3)$" ), address: str = Query(..., max_length=4, regex="^\d{4}$"),  protocol: str = Query("A", max_length=1, regex="^[AUEKL]$")):
    
    status = {}
    status.update({"exitcode": "9"})
    status.update({"result": "FAIL"})
    onoff = ""
    if (action == "on"):
        onoff = "1"
    elif (action == "off"):
        onoff = "0"
    elif (action >= 0 and action <= 255):
        onoff = action
    else:
        status.update({"verbose_result": "Action not allowed"})
        return status

    result = subprocess.run(["he853-static", address, onoff, protocol], capture_output=True, text=True)
    print(result.stdout)
    status.update({"verbose_result": result.stdout })
    status.update({"exitcode": result.returncode })
    if (result.returncode == "0"):
        status.update({"result": "OK"})
    return status
