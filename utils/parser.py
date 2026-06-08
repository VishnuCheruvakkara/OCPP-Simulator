import json 

from dataclasses import dataclass
from typing import Any
from utils.status import OCPPMessageType

@dataclass 
class OCPPMessage:
    """
    Represents a parsed OCPP message.
    """
    msg_type: int
    msg_id: str

    action: str | None = None
    payload: Any = None

    error_code: str | None = None
    error_description: str | None = None

def parse_call(data: list) -> OCPPMessage:
    """
    Parse OCPP CALL message.
    """
    return OCPPMessage(
        msg_type=data[0],
        msg_id=data[1],
        action=data[2],
        payload=data[3]
    )


def parse_call_result(data:list) -> OCPPMessage:
    """
    Parse OCPP CALLRESULT message.
    """
    return OCPPMessage(
        msg_type=data[0],
        msg_id=data[1],
        payload=data[2]
    )


def parse_call_error(data:list) -> OCPPMessage:
    """
    Parse OCPP CALLERROR message
    """
    return OCPPMessage(
        msg_type=data[0],
        msg_id=data[1],
        error_code=data[2],
        error_description=data[3],
        payload=data[4] if len(data) > 4 else None
    )

def parse_message(raw_msg: str) -> OCPPMessage:
    """
    Dispatcher to Convert raw OCPP JSON message into OCPPMessage object.
    """
    data = json.loads(raw_msg)

    msg_type = data[0]

    if msg_type == OCPPMessageType.CALL:
        return parse_call(data)

    elif msg_type == OCPPMessageType.CALLRESULT:
        return parse_call_result(data)

    elif msg_type == OCPPMessageType.CALLERROR:
        return parse_call_error(data)

    raise ValueError(f"Unknown message type: {msg_type}")