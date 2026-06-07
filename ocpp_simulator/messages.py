import json
import uuid 
from config import MODEL,VENDOR

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

def heartbeat():
    return json.dumps([
        2,
        new_id(),
        "Heartbeat",
        {}
    ])