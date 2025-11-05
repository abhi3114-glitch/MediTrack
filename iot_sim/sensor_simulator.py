import time
import random
import requests
import datetime

# Your FastAPI endpoint
BACKEND_URL = "http://127.0.0.1:8000/ingest"

# How often to send readings (in seconds)
INTERVAL = 5

def generate_reading():
    """Generate a random but realistic reading"""
    hr = random.randint(60, 140)
    spo2 = round(random.uniform(85, 100), 1)
    temp = round(random.uniform(36.0, 40.5), 1)
    return {
        "timestamp": time.time(),
        "hr": hr,
        "spo2": spo2,
        "temp": temp
    }

def send_to_backend(reading):
    """POST reading to MediTrack backend"""
    try:
        response = requests.post(BACKEND_URL, json=reading)
        if response.status_code == 200:
            data = response.json()
            status = data.get("status", "unknown")
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Sent | HR={reading['hr']} | SpO₂={reading['spo2']} | Temp={reading['temp']}°C | Status={status}")
        else:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ⚠️ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Failed to send reading: {e}")

def main():
    print("MediTrack IoT Sensor Simulator Started")
    print(f"Streaming live vitals every {INTERVAL} seconds...\n")

    while True:
        reading = generate_reading()
        send_to_backend(reading)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
