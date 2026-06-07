import asyncio
import websockets
from config import OCPP_URL,CONNECTOR_ID
from utils.logger import logger, log_message, track_message, send_message
from utils.status import ChargePointStatus, OCPPMessageType, OCPPAction
from .messages import boot_notification,status_notification
from .heartbeat import heartbeat_loop


async def run():
    logger.info(f"Connecting to: {OCPP_URL}")
    try:
        async with websockets.connect(OCPP_URL, subprotocols=["ocpp1.6"]) as ws:
            logger.info("Connected!")

            boot_msg = boot_notification()

            await send_message(ws, boot_msg, OCPPAction.BOOT_NOTIFICATION.value)
            
            heartbeat_started = False
            while True:
                try:
                    msg = await ws.recv()
                    data = log_message(msg)
                    
                    
                    if(data[0] == OCPPMessageType.CALLRESULT.value and isinstance(data[2],dict) and "interval" in data[2] and not heartbeat_started):
                        heartbeat_started = True 

                        interval = data[2]["interval"]

                        logger.info(f"Heartbeat interval is : {interval}")

                        asyncio.create_task(
                            heartbeat_loop(ws, interval)
                        )

                        status_msg = status_notification(
                            ChargePointStatus.AVAILABLE,CONNECTOR_ID
                        )
                        
                        track_message(status_msg, OCPPAction.STATUS_NOTIFICATION.value)

                        await send_message(ws, status_msg, OCPPAction.STATUS_NOTIFICATION.value)
            
                        logger.info("Status -> Available")
                except asyncio.CancelledError:
                    logger.info("Receiver cancelled")
                    break 
    except asyncio.CancelledError:
        logger.info("Client cancelled")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Websocket closed cleanly")
