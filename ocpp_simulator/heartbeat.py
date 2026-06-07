import asyncio

from utils.logger import logger 
from ocpp_simulator.messages import heartbeat

async def heartbeat_loop(ws,interval):
    while True:
        await asyncio.sleep(interval)
        await ws.send(heartbeat())
        logger.info("Heatbeat sent")
        