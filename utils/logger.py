import logging
import json
from utils.state import pending
from utils.parser import parse_message, OCPPMessage
from utils.status import OCPPMessageType

CYAN = "\033[96m"
RESET = "\033[0m"

class PrettyFormatter(logging.Formatter):
    """
    Format log record for pretty console output.
    """
    def format(self, record: logging.LogRecord) -> str:
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

def log_message(msg: str) -> OCPPMessage:
    """
    Parse and log incoming OCPP message from server.
    """
    parsed = parse_message(msg)

    msg_type = parsed.msg_type
    msg_id= parsed.msg_id

    if msg_type == OCPPMessageType.CALLRESULT:
        action = pending.get(msg_id,"Message")

        logger.info(msg,extra={"direction":"RX","action":f"{action}.conf"})
    elif msg_type == OCPPMessageType.CALL:
        action = parsed.action

        logger.info(msg,extra={"direction":"RX", "action": action})

    return parsed

def send_message(ws,msg: str,action:str):
    """
    Parse,log and send outgoing OCPP message from charging pointer.
    """
    track_message(msg,action)

    logger.info(msg, extra={"direction":"TX", "action": action})

    return ws.send(msg)

def track_message(msg: str, action_name: str) -> str:
    """
    Store message id and action in global state pending requests.
    """
    parsed = parse_message(msg)
    msg_id = parsed.msg_id
    pending[msg_id] = action_name 
    return msg_id 
