import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

export default function Home() {
  const [data, setData] = useState([]);
  const [status, setStatus] = useState("normal");

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      setStatus(msg.status);
      setData((prev) => [...prev.slice(-15), msg.data]); // last 15 readings
    };
    return () => ws.close();
  }, []);

  const chartData = {
    labels: data.map((r) =>
      new Date(r.timestamp * 1000).toLocaleTimeString("en-IN", { hour12: false })
    ),
    datasets: [
      {
        label: "Heart Rate (bpm)",
        data: data.map((r) => r.hr),
        borderColor: "rgb(255, 99, 132)",
        tension: 0.4,
      },
      {
        label: "SpO₂ (%)",
        data: data.map((r) => r.spo2),
        borderColor: "rgb(54, 162, 235)",
        tension: 0.4,
      },
      {
        label: "Temperature (°C)",
        data: data.map((r) => r.temp),
        borderColor: "rgb(255, 206, 86)",
        tension: 0.4,
      },
    ],
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <motion.h1
        className="text-4xl font-bold text-center mb-6"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        🩺 MediTrack Dashboard
      </motion.h1>

      <div className="flex flex-col items-center gap-6">
        <motion.div
          className={`text-2xl font-semibold px-6 py-3 rounded-xl shadow-lg ${
            status === "fatal"
              ? "bg-red-600 animate-pulse"
              : "bg-green-600"
          }`}
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
        >
          STATUS: {status.toUpperCase()}
        </motion.div>

        <div className="w-full md:w-3/4 lg:w-1/2 bg-gray-800 rounded-xl p-4 shadow-lg">
          <Line data={chartData} />
        </div>
      </div>

      <motion.div
        className="mt-10 text-center text-sm opacity-70"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <p>⛓️ Blockchain Verified | FastAPI + IoT + AI + Web3 Integration</p>
      </motion.div>
    </div>
  );
}
