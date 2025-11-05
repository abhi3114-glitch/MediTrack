"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

export default function Page() {
  const [data, setData] = useState([]);
  const [status, setStatus] = useState("normal");
  const [logs, setLogs] = useState([]);
  const [latestHash, setLatestHash] = useState(null);
  const [alertCause, setAlertCause] = useState(null);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      setStatus(msg.status);
      setData((prev) => [...prev.slice(-20), msg.data]);

      const hrRisk = msg.data.hr > 120 ? 80 : msg.data.hr / 2;
      const tempRisk = msg.data.temp > 39 ? 70 : msg.data.temp * 2;
      const risk = Math.min(Math.max((hrRisk + tempRisk) / 2, 0), 100);

      const logMsg =
        msg.status === "fatal"
          ? `FATAL EVENT — HR:${msg.data.hr} | SpO₂:${msg.data.spo2} | Temp:${msg.data.temp}`
          : `Normal Update — HR:${msg.data.hr} | SpO₂:${msg.data.spo2} | Temp:${msg.data.temp}`;

      setLogs((prev) => [
        { time: new Date().toLocaleTimeString(), message: logMsg },
        ...prev.slice(0, 15),
      ]);

      setLatestHash(msg.hash || latestHash);
      setAlertCause(msg.cause || null);
    };
    return () => ws.close();
  }, []);

  useEffect(() => {
    if (status === "fatal") {
      const audio = new Audio("/alert.mp3");
      audio.play();
    }
  }, [status]);

  const chartData = {
    labels: data.map((r) =>
      new Date(r.timestamp * 1000).toLocaleTimeString("en-IN", {
        hour12: false,
        minute: "2-digit",
        second: "2-digit",
      })
    ),
    datasets: [
      {
        label: "Heart Rate (bpm)",
        data: data.map((r) => r.hr),
        borderColor: "#ff497c",
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0,
      },
      {
        label: "SpO₂ (%)",
        data: data.map((r) => r.spo2),
        borderColor: "#2bc3ff",
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0,
      },
      {
        label: "Temperature (°C)",
        data: data.map((r) => r.temp),
        borderColor: "#ffd54f",
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0,
      },
    ],
  };

  return (
    <div className="min-h-screen bg-[#060b17] text-white flex flex-col items-center">
      {/* HEADER BAR */}
      <div className="holo-lite p-3 mb-5 flex justify-between items-center w-full max-w-[1300px] rounded-xl text-sm opacity-80">
        <span>Device ID: MT-001</span>
        <span>Patient: Abhishek</span>
        <span>Connected Node: Ganache:7545</span>
      </div>

      {/* MAIN WRAPPER */}
      <div className="main-container grid grid-cols-1 lg:grid-cols-[1fr_1.6fr_1fr] gap-6">
        {/* LEFT PANEL */}
        <motion.div
          className="holo p-6 rounded-2xl flex flex-col justify-between fadeIn"
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 1 }}
        >
          <div>
            <h1 className="text-4xl font-bold mb-2 text-cyan-400">MediTrack</h1>
            <p className="text-sm opacity-70 mb-6 leading-relaxed">
              Real-time IoT health monitoring with AI alerts and blockchain logging.
            </p>

            <div
              className={`text-xl font-semibold text-center py-3 px-6 rounded-lg tracking-wider ${
                status === "fatal" ? "status-fatal" : "status-normal"
              }`}
            >
              STATUS: {status.toUpperCase()}
            </div>

            {alertCause && (
              <p className="mt-3 text-center text-sm text-red-400">{alertCause}</p>
            )}

            {data.length > 0 && (
              <div className="mt-8 space-y-4">
                <div className="holo-lite p-3 rounded-md flex justify-between live-change">
                  <span>Heart Rate</span>
                  <span className="font-semibold text-pink-400">
                    {data.at(-1)?.hr} bpm
                  </span>
                </div>
                <div className="holo-lite p-3 rounded-md flex justify-between live-change">
                  <span>SpO₂</span>
                  <span className="font-semibold text-sky-400">
                    {data.at(-1)?.spo2}%
                  </span>
                </div>
                <div className="holo-lite p-3 rounded-md flex justify-between live-change">
                  <span>Temperature</span>
                  <span className="font-semibold text-amber-400">
                    {data.at(-1)?.temp}°C
                  </span>
                </div>
              </div>
            )}

            {/* RISK INDICATOR */}
            <div className="mt-8">
              <p className="text-sm mb-2 text-cyan-300">AI Risk Indicator</p>
              <div className="w-full bg-gray-800 rounded-full h-3">
                <div
                  className={`h-3 rounded-full transition-all duration-500 ${
                    status === "fatal" ? "bg-red-500" : "bg-green-400"
                  }`}
                  style={{
                    width: status === "fatal" ? "85%" : "35%",
                  }}
                ></div>
              </div>
            </div>
          </div>

          <div className="mt-10 text-xs opacity-60 text-center">
            Blockchain Verified • FastAPI • IoT • AI • Web3
            {latestHash && (
              <div className="mt-2 text-cyan-400">
                TX: {latestHash.slice(0, 10)}...
              </div>
            )}
            <div className="footer-credit">Developed by Abhishek</div>
          </div>
        </motion.div>

        {/* CENTER PANEL */}
        <motion.div
          className="holo p-6 rounded-2xl fadeIn flex flex-col justify-between"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          <h2 className="text-2xl mb-5 font-semibold text-center text-cyan-300">
            Live Vital Trends
          </h2>

          <div className="bg-[#0e1628]/60 p-6 rounded-2xl flex-grow">
            <Line
              data={chartData}
              options={{
                plugins: {
                  legend: {
                    labels: { color: "white", font: { size: 12 } },
                  },
                },
                scales: {
                  x: {
                    ticks: { color: "#aaa" },
                    grid: { color: "rgba(255,255,255,0.05)" },
                  },
                  y: {
                    ticks: { color: "#aaa" },
                    grid: { color: "rgba(255,255,255,0.05)" },
                  },
                },
                maintainAspectRatio: false,
              }}
              height={300}
            />
          </div>
        </motion.div>

        {/* RIGHT PANEL */}
        <motion.div
          className="holo p-6 rounded-2xl fadeIn flex flex-col"
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 1 }}
        >
          <h2 className="text-2xl mb-4 font-semibold text-cyan-300 text-center">
            System Activity
          </h2>

          <div
            className="overflow-y-auto space-y-3 pr-2 custom-scroll"
            style={{
              maxHeight: "65vh",
              scrollBehavior: "smooth",
            }}
          >
            {logs.map((log, idx) => (
              <div
                key={idx}
                className={`text-sm p-3 rounded-md border-l-4 ${
                  log.message.includes("FATAL")
                    ? "border-red-500 bg-red-500/10"
                    : "border-green-400 bg-green-400/10"
                }`}
              >
                <p className="text-xs opacity-70">{log.time}</p>
                <p className="mt-1">{log.message}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
