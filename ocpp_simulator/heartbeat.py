import asyncio

from utils.logger import logger, track_message, send_message
from utils.status import OCPPAction
from ocpp_simulator.messages import heartbeat

async def heartbeat_loop(ws,interval):
    while True:
        await asyncio.sleep(interval)
        heartbeat_msg = heartbeat()

        track_message(heartbeat_msg, OCPPAction.HEARTBEAT.value)
        
        await send_message(ws, heartbeat_msg, OCPPAction.HEARTBEAT.value)
        