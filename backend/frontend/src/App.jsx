import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [messages, setMessages] = useState([
    {
      sender: "agent",
      text: "Hello! How can I assist you with orders, catalog items, or store policies?",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/chat", {
        message: input,
      });
      setMessages((prev) => [
        ...prev,
        { sender: "agent", text: res.data.reply },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "agent",
          text: "Error connecting to the support server. Ensure the backend is running on port 8000.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: 640,
        margin: "40px auto",
        fontFamily: "Segoe UI, sans-serif",
      }}
    >
      <h2>Customer Support Assistant</h2>
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: 8,
          height: 420,
          overflowY: "auto",
          padding: 16,
        }}
      >
        {messages.map((m, idx) => (
          <div
            key={idx}
            style={{
              textAlign: m.sender === "user" ? "right" : "left",
              margin: "8px 0",
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "10px 14px",
                borderRadius: 8,
                maxWidth: "80%",
                textAlign: "left",
                whiteSpace: "pre-wrap",
                lineHeight: "1.5",
                background: m.sender === "user" ? "#007bff" : "#f0f0f0",
                color: m.sender === "user" ? "#fff" : "#000",
              }}
            >
              {m.text}
            </span>
          </div>
        ))}
        {loading && (
          <p style={{ fontStyle: "italic", color: "#888" }}>
            Agent is checking...
          </p>
        )}
      </div>
      <div style={{ display: "flex", marginTop: 12, gap: 8 }}>
        <input
          style={{ flex: 1, padding: "10px 12px", fontSize: 14 }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Track ORD1001, search headphones, or ask policy..."
        />
        <button
          style={{ padding: "10px 20px", cursor: "pointer" }}
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}
