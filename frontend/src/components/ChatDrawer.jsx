import React, { useState } from "react";
import { api } from "../api";

export default function ChatDrawer({ isOpen, onClose }) {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! Ask me for CD recommendations or catalog questions." },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);

  if (!isOpen) return null;

  const handleSend = async (e) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMsg = { sender: "user", text: trimmed };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setSending(true);

    try {
      const res = await api.sendChatMessage(trimmed);
      setMessages((prev) => [...prev, { sender: "bot", text: res.reply }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: `Unable to reach assistant: ${err.message}` },
      ]);
    } finally {
      setSending(false);
    }
  };

  return (
    <aside
      style={{
        position: "fixed",
        top: 0,
        right: 0,
        width: "340px",
        height: "100vh",
        background: "#ffffff",
        borderLeft: "1px solid #e2e8f0",
        boxShadow: "-4px 0 15px rgba(0,0,0,0.08)",
        display: "flex",
        flexDirection: "column",
        zIndex: 40,
      }}
    >
      <div
        style={{
          padding: "1rem",
          borderBottom: "1px solid #e2e8f0",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h3 style={{ margin: 0 }}>AI Music Assistant</h3>
        <button
          onClick={onClose}
          style={{ background: "transparent", border: "none", fontSize: "1.2rem", cursor: "pointer" }}
        >
          ✕
        </button>
      </div>

      <div style={{ flex: 1, padding: "1rem", overflowY: "auto", display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
              background: msg.sender === "user" ? "#2563eb" : "#f1f5f9",
              color: msg.sender === "user" ? "#ffffff" : "#0f172a",
              padding: "0.6rem 0.85rem",
              borderRadius: "8px",
              maxWidth: "85%",
              fontSize: "0.9rem",
            }}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <form
        onSubmit={handleSend}
        style={{
          padding: "0.75rem",
          borderTop: "1px solid #e2e8f0",
          display: "flex",
          gap: "0.5rem",
        }}
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about an album or genre..."
          style={{
            flex: 1,
            padding: "0.5rem",
            borderRadius: "6px",
            border: "1px solid #cbd5e1",
          }}
        />
        <button
          type="submit"
          disabled={sending}
          style={{
            background: "#2563eb",
            color: "#ffffff",
            border: "none",
            borderRadius: "6px",
            padding: "0.5rem 0.85rem",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </form>
    </aside>
  );
}

