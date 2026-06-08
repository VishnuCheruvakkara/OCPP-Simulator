import json
import uuid 
from config import MODEL,VENDOR
from utils.status import OCPPAction, OCPPMessageType

def new_id() -> str:
    """
    Generate a unique OCPP message id.
    """
    return str(uuid.uuid4())

def boot_notification() -> str:
    """
    Create BootNotification request message.
    """
    return json.dumps([
        OCPPMessageType.CALL,
        new_id(),
        OCPPAction.BOOT_NOTIFICATION.value,
        {
            "chargePointModel":MODEL,
            "chargePointVendor":VENDOR
        }
    ])

def heartbeat() -> str:
    """
    Create Heartbeat request message.
    """
    return json.dumps([
        OCPPMessageType.CALL,
        new_id(),
        OCPPAction.HEARTBEAT.value,
        {}
    ])

def status_notification(status,connector_id: int) -> str:
    """
    Create StatusNotification request message.
    """
    return json.dumps([
        OCPPMessageType.CALL,
        new_id(),
        OCPPAction.STATUS_NOTIFICATION.value,
        {
            "connectorId": connector_id,
            "errorCode":"NoError",
            "status": status.value
        }
    ])