import asyncio
import websockets
from config import OCPP_URL,MODEL,VENDOR
from utils.logger import logger 
from .messages import boot_notification
from .heartbeat import heartbeat_loop
import json 

async def run():
    logger.info(f"Connecting to: {OCPP_URL}")
    try:
        async with websockets.connect(OCPP_URL, subprotocols=["ocpp1.6"]) as ws:
            logger.info("Connected!")

            await ws.send(boot_notification())
            logger.info("BootNotification sent!")
            
            heartbeat_started = False
            while True:
                try:
                    msg = await ws.recv()
                    logger.info(f"Server: {msg}")
                    data = json.loads(msg)
                    
                    if(data[0] == 3 and isinstance(data[2],dict) and "interval" in data[2] and not heartbeat_started):
                        heartbeat_started = True 

                        interval = data[2]["interval"]

                        logger.info(f"Heartbeat interval is : {interval}")

                        asyncio.create_task(
                            heartbeat_loop(ws, interval)
                        )
                except asyncio.CancelledError:
                    logger.info("Receiver cancelled")
                    break 
    except asyncio.CancelledError:
        logger.info("Client cancelled")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Websocket closed cleanly")
