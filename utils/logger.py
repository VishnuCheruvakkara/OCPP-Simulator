import logging
import json

class PrettyFormatter(logging.Formatter):

    def format(self, record):
        msg = record.getMessage()

        try:
            if msg.startswith("Server:"):
                data = msg.replace("Server:", "").strip()
                parsed = json.loads(data)
                pretty = json.dumps(parsed, indent=2)

                return f"{self.formatTime(record)} | {record.levelname} | Server:\n{pretty}"

        except Exception:
            pass

        return f"{self.formatTime(record)} | {record.levelname} | {msg}"


handler = logging.StreamHandler()
handler.setFormatter(PrettyFormatter("%(asctime)s"))

logger = logging.getLogger("ocpp")
logger.setLevel(logging.INFO)

if not logger.handlers:
    logger.addHandler(handler)