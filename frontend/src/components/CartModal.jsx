import React, { useState } from "react";
import { api } from "../api";

export default function CartModal({ isOpen, onClose, cartItems, onClearCart }) {
  const [statusMessage, setStatusMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handleCheckout = async () => {
    setSubmitting(true);
    setStatusMessage("");
    try {
      const res = await api.createOrder(cartItems);
      setStatusMessage(`${res.message} (Order ID: ${res.order.order_id})`);
      onClearCart();
    } catch (err) {
      setStatusMessage(`Checkout error: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(15, 23, 42, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 50,
      }}
    >
      <div
        style={{
          background: "#ffffff",
          borderRadius: "10px",
          padding: "1.5rem",
          width: "90%",
          maxWidth: "460px",
          boxShadow: "0 10px 25px rgba(0,0,0,0.15)",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h2 style={{ margin: 0 }}>Your Shopping Cart</h2>
          <button
            onClick={onClose}
            style={{ background: "transparent", border: "none", fontSize: "1.25rem", cursor: "pointer" }}
          >
            ✕
          </button>
        </div>

        <div style={{ margin: "1rem 0" }}>
          {cartItems.length === 0 ? (
            <p style={{ color: "#64748b" }}>Your cart is currently empty.</p>
          ) : (
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {cartItems.map((item) => (
                <li
                  key={item.id}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    padding: "0.5rem 0",
                    borderBottom: "1px solid #e2e8f0",
                  }}
                >
                  <span>
                    {item.title} × {item.quantity}
                  </span>
                  <strong>${(item.price * item.quantity).toFixed(2)}</strong>
                </li>
              ))}
            </ul>
          )}
        </div>

        {statusMessage && (
          <p style={{ padding: "0.5rem", background: "#f0fdf4", color: "#166534", borderRadius: "6px" }}>
            {statusMessage}
          </p>
        )}

        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "1rem" }}>
          <strong>Total: ${total.toFixed(2)}</strong>
          <button
            disabled={cartItems.length === 0 || submitting}
            onClick={handleCheckout}
            style={{
              background: cartItems.length === 0 ? "#94a3b8" : "#16a34a",
              color: "#ffffff",
              border: "none",
              borderRadius: "6px",
              padding: "0.5rem 1rem",
              cursor: cartItems.length === 0 ? "not-allowed" : "pointer",
            }}
          >
            {submitting ? "Placing Order..." : "Checkout"}
          </button>
        </div>
      </div>
    </div>
  );
}

