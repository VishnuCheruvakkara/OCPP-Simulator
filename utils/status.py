from enum import Enum, IntEnum

class ChargePointStatus(str,Enum):
    AVAILABLE = "Available"
    PREPARING = "Preparing"
    CHARGING = "Charging"
    FINISHING = "Finishing"

class OCPPMessageType(IntEnum):
    CALL = 2 
    CALLRESULT = 3 
    CALLERROR = 4

class OCPPAction(str, Enum):
    BOOT_NOTIFICATION = "BootNotification"
    STATUS_NOTIFICATION = "StatusNotification"
    HEARTBEAT = "Heartbeat"
    DATA_TRANSFER = "DataTransfer"

    REMOTE_START_TRANSACTION = "RemoteStartTransaction"
    REMOTE_STOP_TRANSACTION = "RemoteStopTransaction"
    RESET = "Reset"

    METER_VALUES = "MeterValues"