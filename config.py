import os
from dotenv import load_dotenv

load_dotenv()

OCPP_URL = os.getenv("OCPP_URL")
MODEL = os.getenv("CHARGE_POINT_MODEL")
VENDOR = os.getenv("CHARGE_POINT_VENDOR")