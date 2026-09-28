// Shared helpers for the Control Room admin panel.
// Talks to the existing FastAPI admin API at /api/v1/admin/*.

const API_BASE = "/api/v1/admin";
const TOKEN_KEY = "admin_token";
const NAME_KEY = "admin_name";

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setSession(token, adminname) {
  localStorage.setItem(TOKEN_KEY, token);
  if (adminname) localStorage.setItem(NAME_KEY, adminname);
}

function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(NAME_KEY);
}

function requireAuth() {
  if (!getToken()) {
    window.location.href = "/admin/login";
  }
}

function logout() {
  clearSession();
  window.location.href = "/admin/login";
}

function markActiveNav(key) {
  document.querySelectorAll(".rail-nav a").forEach((a) => {
    if (a.dataset.nav === key) a.classList.add("active");
  });
}

function loadAdminName() {
  const cached = localStorage.getItem(NAME_KEY);
  const el = document.getElementById("adminName");
  if (cached && el) el.textContent = cached;

  // Also verify the token is still valid against the API.
  apiFetch("/getadmin").catch(() => {
    clearSession();
    window.location.href = "/admin/login";
  });
}

function showToast(message, isError = false) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.toggle("error", isError);
  toast.classList.add("show");
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => toast.classList.remove("show"), 3200);
}

/**
 * Fetch wrapper that attaches the admin JWT, builds query strings for
 * GET params, and throws a normalized Error with a `.status` on failure.
 */
async function apiFetch(path, { method = "GET", params = null, body = null } = {}) {
  let url = API_BASE + path;
  if (params) {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== ""))
    ).toString();
    if (qs) url += "?" + qs;
  }

  const headers = { Authorization: "Bearer " + (getToken() || "") };
  if (body) headers["Content-Type"] = "application/json";

  const res = await fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  let data = null;
  try {
    data = await res.json();
  } catch (_) {
    // no JSON body
  }

  if (res.status === 401) {
    clearSession();
    window.location.href = "/admin/login";
    throw new Error("Unauthorized");
  }

  if (!res.ok) {
    const err = new Error((data && data.detail) || `Request failed (${res.status})`);
    err.status = res.status;
    throw err;
  }

  return data;
}

// `isban` is a Peewee CharField defaulting to the boolean False, so it can
// come back from the API as an actual bool OR as the string "False"/"True"
// depending on how it was written. Treat both shapes as valid.
function isBanned(u) {
  return u.isban === true || u.isban === "True" || u.isban === "true";
}

function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}