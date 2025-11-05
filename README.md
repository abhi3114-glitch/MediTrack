# 🩺 MediTrack
**Real-Time IoT Health Monitoring System with AI Alerts, Blockchain Logging & Telegram Notifications**

---

## 🚀 Overview
**MediTrack** is an advanced **real-time patient monitoring system** that integrates **IoT simulation**, **AI-driven health analysis**, **FastAPI backend**, **Next.js dashboard**, and **Ethereum blockchain (Ganache)** for immutable record logging.

It detects **abnormal/fatal vital readings**, sends **instant Telegram alerts**, updates **live charts on dashboard**, and stores **tamper-proof health records** on the blockchain.

---

## 🧠 Key Features

### 🩸 Real-Time Health Monitoring
- Continuously receives **IoT sensor readings** (Heart Rate, SpO₂, Temperature).  
- Detects **critical thresholds** like heart rate spikes, oxygen drops, or fever.  

### ⚠️ AI-Driven Alerts
- Automatically classifies each reading as **Normal** or **Fatal**.  
- Displays **alert cause** (e.g., “Severe oxygen drop detected”).  

### 🔔 Telegram Notifications
- Sends **immediate Telegram alerts** to doctors/family with live vitals.  
- Uses **Bot API** and environment-secure tokens.  

### ⛓️ Blockchain Integration
- Stores **hashed patient readings** on the **Ethereum test blockchain (Ganache)**.  
- Ensures **data immutability** and **tamper resistance**.

### 📊 Live Web Dashboard
- Built with **Next.js 16 + Tailwind + Chart.js**.  
- Displays **real-time vital graphs**, **system activity logs**, and **blockchain verification** status.  

### 🧪 IoT Sensor Simulator
- Generates **synthetic but realistic** vitals for testing.  
- Mimics an actual wearable IoT health device.

---

## 🏗️ System Architecture

```
IoT Sensor Simulator  →  FastAPI Backend  →  Telegram Alerts
                                 ↓
                      Blockchain Ledger (Ganache)
                                 ↓
                        Next.js Web Dashboard
```

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend API** | FastAPI (Python) |
| **Frontend Dashboard** | Next.js (React + TailwindCSS) |
| **Blockchain** | Ethereum (Ganache + web3.py + Solidity) |
| **Database** | SQLite |
| **AI Logic** | Custom rule-based + analytics |
| **Alerts** | Telegram Bot API |
| **IoT Simulation** | Python random signal generator |

---

## 🧩 Folder Structure

```
MEDITRACK/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── blockchain/
│   │       ├── deploy_contract.py
│   │       └── contract_interact.py
│   ├── meditrack.db
│   └── .env
│
├── frontend/
│   └── dashboard/
│       ├── app/page.js
│       ├── styles/global.css
│       └── public/alert.mp3
│
├── iot_sim/
│   └── sensor_simulator.py
│
├── run_meditrack.py (optional)
└── README.md
```

---

## 🔧 Installation & Setup

### 1️⃣ Clone & Setup Environment
```bash
git clone https://github.com/<your-username>/MediTrack.git
cd MEDITRACK
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### 2️⃣ Configure `.env`

```env
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_CHAT_ID
GANACHE_URL=http://127.0.0.1:7545
```

---

### 3️⃣ Start Ganache
Run Ganache GUI and ensure it's active on **http://127.0.0.1:7545**.

---

### 4️⃣ Deploy Smart Contract
```bash
cd backend/app/blockchain
python deploy_contract.py
```

---

### 5️⃣ Start Backend
```bash
uvicorn backend.app.main:app --reload --port 8000
```

---

### 6️⃣ Run IoT Simulator
```bash
cd iot_sim
python sensor_simulator.py
```

---

### 7️⃣ Start Frontend Dashboard
```bash
cd frontend/dashboard
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000)

---

## 💬 Example Telegram Alert

```
🚨 MediTrack Fatal Alert!
💓 HR: 135 bpm
🩸 SpO₂: 85%
🌡️ Temp: 39.5°C
⚠️ Cause: Severe oxygen drop detected
🕒 18:42:10
```

---

## 🧾 Future Enhancements
- Integrate real IoT hardware sensors (MAX30100, DHT11, ESP32)
- Add historical health tracking and doctor dashboard
- Implement predictive ML models
- Deploy on testnet / Polygon network

---

## 👨‍💻 Developed By
**Abhishek Pratap Singh Chauhan**  
