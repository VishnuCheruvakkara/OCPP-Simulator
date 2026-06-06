import asyncio
import json
import uuid 
import websockets
from config import OCPP_URL,MODEL,VENDOR

def new_id():
    return str(uuid.uuid4())

def boot_notification():
    return json.dumps([
        2,
        new_id(),
        "BootNotification",
        {
            "chargePointModel":MODEL,
            "chargePointVendor":VENDOR
        }
    ])

async def run():
    print("Connecting to:", OCPP_URL)
    try:
        async with websockets.connect(OCPP_URL, subprotocols=["ocpp1.6"]) as ws:
            print("Connected!")

            await ws.send(boot_notification())
            print("BootNotification sent!")

            while True:
                try:
                    msg = await ws.recv()
                    print("Server:",msg)
                except asyncio.CancelledError:
                    print("Receiver cancelled")
                    break 
    except asyncio.CancelledError:
        print("Client cancelled")
    except Exception as e:
        print("Error:", e)
    finally:
        print("Websocket closed cleanly")
