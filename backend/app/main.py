from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import sqlite3, json, hashlib, requests, os, asyncio, datetime

# ───────────────────────────────────────────────
# 🔗 Blockchain imports
try:
    from app.blockchain.contract_interact import add_record_hex
    blockchain_enabled = True
except Exception as e:
    print("⚠️ Blockchain integration not available:", e)
    blockchain_enabled = False
# ───────────────────────────────────────────────

load_dotenv()

app = FastAPI()

# Allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

active_connections = []

# ───────────────────────────────────────────────
# 📩 Telegram alert function
def send_telegram_alert(message: str):
    """Send alert message to Telegram."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=data)
        print("✅ Telegram alert sent")
    except Exception as e:
        print("⚠️ Error sending Telegram alert:", e)

# 🪙 Blockchain background function
def add_to_blockchain(record_hash: str):
    """Add record hash to blockchain ledger."""
    if not blockchain_enabled:
        print("⚠️ Blockchain not available.")
        return
    try:
        print("⛓️ Adding record to blockchain:", record_hash)
        result = add_record_hex(record_hash)
        print("✅ Blockchain TX:", result)
    except Exception as e:
        print("⚠️ Blockchain write failed:", e)
# ───────────────────────────────────────────────


def init_db():
    conn = sqlite3.connect("meditrack.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY,
        ts REAL,
        hr INTEGER,
        spo2 REAL,
        temp REAL,
        status TEXT,
        hash TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()


class Reading(BaseModel):
    timestamp: float
    hr: int
    spo2: float
    temp: float


@app.post("/ingest")
async def ingest(reading: Reading, background_tasks: BackgroundTasks):
    payload = json.dumps(reading.dict(), sort_keys=True)
    record_hash = hashlib.sha256(payload.encode()).hexdigest()

    status = "normal"
    msg = None
    cause = None  # initialize

    # 🚨 Detect fatal cases + add specific cause
    if reading.hr > 120:
        cause = "Heart rate spike detected"
    elif reading.spo2 < 88:
        cause = "Severe oxygen drop detected"
    elif reading.temp > 39:
        cause = "High fever detected"

    if cause:
        status = "fatal"
        msg = (
            f"🚨 *MediTrack Fatal Alert!* 🚨\n"
            f"💓 HR: {reading.hr} bpm\n"
            f"🩸 SpO₂: {reading.spo2}%\n"
            f"🌡️ Temp: {reading.temp}°C\n"
            f"⚠️ Cause: {cause}\n"
            f"🕒 {datetime.datetime.now().strftime('%H:%M:%S')}"
        )

        # Background tasks for Telegram + Blockchain
        background_tasks.add_task(send_telegram_alert, msg)
        background_tasks.add_task(add_to_blockchain, record_hash)

    # 🧠 Store in DB
    conn = sqlite3.connect("meditrack.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO readings (ts, hr, spo2, temp, status, hash) VALUES (?,?,?,?,?,?)",
        (reading.timestamp, reading.hr, reading.spo2, reading.temp, status, record_hash),
    )
    conn.commit()
    conn.close()

    # Broadcast to all dashboard clients
    enriched_data = reading.dict()
    enriched_data["cause"] = cause
    await broadcast_to_dashboards(enriched_data, status)

    return {"status": status, "hash": record_hash, "cause": cause}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except Exception:
        pass
    finally:
        active_connections.remove(websocket)


async def broadcast_to_dashboards(data, status):
    """Send live updates to all dashboards"""
    message = json.dumps({"data": data, "status": status})
    for conn in active_connections:
        try:
            await conn.send_text(message)
        except Exception:
            pass
