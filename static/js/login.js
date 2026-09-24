// If already signed in, skip straight to the dashboard.
if (getToken()) {
  window.location.href = "/admin/dashboard";
}

const form = document.getElementById("loginForm");
const errorEl = document.getElementById("loginError");
const btn = document.getElementById("loginBtn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorEl.textContent = "";
  btn.disabled = true;
  btn.textContent = "Signing in…";

  const adminname = document.getElementById("adminname").value.trim();
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("/api/v1/admin/adminlogin", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ adminname, password }),
    });
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Sign in failed");
    }

    setSession(data.token, adminname);
    window.location.href = "/admin/dashboard";
  } catch (err) {
    errorEl.textContent = err.message || "Sign in failed";
    btn.disabled = false;
    btn.textContent = "Sign in";
  }
});
