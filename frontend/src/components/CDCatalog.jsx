import React from "react";

export default function CDCatalog({ cds, loading, error, onAddToCart }) {
  if (loading) {
    return <p>Loading CD catalog...</p>;
  }

  if (error) {
    return (
      <div style={{ padding: "1rem", background: "#fee2e2", color: "#991b1b", borderRadius: "8px" }}>
        <strong>Error loading catalog:</strong> {error}
      </div>
    );
  }

  return (
    <section>
      <h2 style={{ marginBottom: "1rem" }}>Available CDs</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          gap: "1rem",
        }}
      >
        {cds.map((cd) => (
          <div
            key={cd.id}
            style={{
              background: "#ffffff",
              border: "1px solid #e2e8f0",
              borderRadius: "8px",
              padding: "1rem",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <h3 style={{ margin: "0 0 0.25rem 0", fontSize: "1.1rem" }}>{cd.title}</h3>
              <p style={{ margin: "0 0 0.5rem 0", color: "#475569" }}>{cd.artist}</p>
              <span
                style={{
                  display: "inline-block",
                  fontSize: "0.75rem",
                  background: "#f1f5f9",
                  padding: "0.2rem 0.5rem",
                  borderRadius: "4px",
                  color: "#334155",
                }}
              >
                {cd.genre}
              </span>
            </div>
            <div style={{ marginTop: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <strong style={{ fontSize: "1.1rem" }}>${cd.price.toFixed(2)}</strong>
              <button
                onClick={() => onAddToCart(cd)}
                style={{
                  background: "#2563eb",
                  color: "#ffffff",
                  border: "none",
                  borderRadius: "6px",
                  padding: "0.45rem 0.85rem",
                  cursor: "pointer",
                }}
              >
                Add to Cart
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

