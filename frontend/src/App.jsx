import React, { useEffect, useState } from "react";
import { api } from "./api";
import CDCatalog from "./components/CDCatalog";
import CartModal from "./components/CartModal";
import ChatDrawer from "./components/ChatDrawer";

export default function App() {
  const [cds, setCds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);

  useEffect(() => {
    api
      .getCDs()
      .then((res) => {
        setCds(res.data || []);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const handleAddToCart = (cd) => {
    setCart((prev) => {
      const existing = prev.find((item) => item.id === cd.id);
      if (existing) {
        return prev.map((item) =>
          item.id === cd.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      return [...prev, { ...cd, quantity: 1 }];
    });
  };

  const totalCartItems = cart.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <header
        style={{
          background: "#0f172a",
          color: "#ffffff",
          padding: "1rem 2rem",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h1 style={{ margin: 0, fontSize: "1.35rem" }}>💿 CD Online Store</h1>
        <div style={{ display: "flex", gap: "0.75rem" }}>
          <button
            onClick={() => setIsCartOpen(true)}
            style={{
              background: "#334155",
              color: "#ffffff",
              border: "none",
              borderRadius: "6px",
              padding: "0.5rem 0.9rem",
              cursor: "pointer",
            }}
          >
            🛒 Cart ({totalCartItems})
          </button>
          <button
            onClick={() => setIsChatOpen((prev) => !prev)}
            style={{
              background: "#2563eb",
              color: "#ffffff",
              border: "none",
              borderRadius: "6px",
              padding: "0.5rem 0.9rem",
              cursor: "pointer",
            }}
          >
            💬 AI Assistant
          </button>
        </div>
      </header>

      <main style={{ maxWidth: "1080px", width: "100%", margin: "0 auto", padding: "2rem", boxSizing: "border-box" }}>
        <CDCatalog
          cds={cds}
          loading={loading}
          error={error}
          onAddToCart={handleAddToCart}
        />
      </main>

      <CartModal
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        cartItems={cart}
        onClearCart={() => setCart([])}
      />

      <ChatDrawer
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
      />
    </div>
  );
}

