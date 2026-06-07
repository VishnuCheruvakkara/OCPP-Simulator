# OCPP 1.6 Charge Point Simulator

A simple Python simulator for OCPP 1.6 JSON over WebSocket charge point behavior.

## Structure

- `README.md` — project overview and run instructions
- `requirements.txt` — Python dependencies
- `main.py` — entry point
- `config.py` — environment / CLI configuration
- `ocpp_simulator/` — simulator implementation
  - `connection.py` — WebSocket connection, reconnect, subprotocol
  - `message.py` — OCPP JSON framing, request/response correlation
  - `session.py` — charging session state machine and heartbeat
  - `handlers.py` — server request handlers (start/stop/reset)
  - `utils.py` — helpers for time, energy, logging

## Run

1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Set environment variables or use `.env` / `.env.example`.
4. Run the simulator:
   ```bash
   python main.py
   ```

## Notes

- Use `OCPP_URL` and `CHARGE_POINT_ID` to configure the server URL and charge point ID.
- This project is designed to keep the OCPP message handling separate from session flow.
