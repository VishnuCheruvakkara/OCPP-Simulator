import logging
import json
from utils.state import pending

CYAN = "\033[96m"
RESET = "\033[0m"

class PrettyFormatter(logging.Formatter):

    def format(self, record):
        msg = record.getMessage()

        header = f"{self.formatTime(record)} | {record.levelname}"

        try:
            header += f" | {record.direction} | {record.action}"
        except:
            pass

        header = f"\033[96m{header}\033[0m"

        try:
            data = json.loads(msg)
            return f"{header}\n{json.dumps(data, indent=2)}"
        except:
            return f"{header} | {msg}"


handler = logging.StreamHandler()
handler.setFormatter(PrettyFormatter("%(asctime)s"))

logger = logging.getLogger("ocpp")
logger.setLevel(logging.INFO)

if not logger.handlers:
    logger.addHandler(handler)


def log_message(msg):
    data = json.loads(msg)
    msg_type = data[0]
    msg_id=data[1]

    if msg_type == 3:
        action = pending.get(msg_id,"Message")

        logger.info(msg,extra={"direction":"RX","action":f"{action}.conf"})
    elif msg_type == 2:
        action = data[2]

        logger.info(msg,extra={"direction":"RX", "action": action})

    return data

def send_message(ws,msg,action):
    data = json.loads(msg)
    msg_id = data[1]

    pending[msg_id] = action

    logger.info(msg, extra={"direction":"TX", "action": action})

    return ws.send(msg)

def track_message(msg, action_name):
    data = json.loads(msg)
    msg_id = data[1]
    pending[msg_id] = action_name 
    return msg_id 
