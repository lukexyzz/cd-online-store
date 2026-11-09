const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api";

/**
 * Centralised fetch helper for communicating with the Flask REST API backend.
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const defaultHeaders = {
    "Content-Type": "application/json",
  };

  const response = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...(options.headers || {}),
    },
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.message || `API request failed with status ${response.status}`);
  }
  return data;
}

export const api = {
  getCDs: () => request("/cds", { method: "GET" }),
  createOrder: (items) =>
    request("/orders", {
      method: "POST",
      body: JSON.stringify({ items }),
    }),
  sendChatMessage: (message) =>
    request("/chat", {
      method: "POST",
      body: JSON.stringify({ message }),
    }),
};

