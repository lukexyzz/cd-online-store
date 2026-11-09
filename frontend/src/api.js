const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api";

/**
 * Centralised fetch helper for communicating with the Flask REST API backend.
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = localStorage.getItem("auth_token");
  const defaultHeaders = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
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
    throw new Error(data.error || data.message || `API request failed with status ${response.status}`);
  }
  return data;
}

export const api = {
  register: (email, password) =>
    request("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  login: async (email, password) => {
    const res = await request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    if (res.token) {
      localStorage.setItem("auth_token", res.token);
    }
    return res;
  },
  logout: () => {
    localStorage.removeItem("auth_token");
  },
  getCDs: () => request("/cds", { method: "GET" }),
  createOrder: (items) =>
    request("/orders", {
      method: "POST",
      body: JSON.stringify({ items }),
    }),
  sendChatMessage: (message, sessionId = "default_session") =>
    request("/chat", {
      method: "POST",
      body: JSON.stringify({ message, session_id: sessionId }),
    }),
};
