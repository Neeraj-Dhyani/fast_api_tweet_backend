let allUsers = [];

function renderUsers(users) {
  const body = document.getElementById("usersBody");

  if (!users.length) {
    body.innerHTML = `<tr><td colspan="4" class="empty-row">No users found.</td></tr>`;
    return;
  }

  body.innerHTML = users
    .map((u) => {
      const banned = isBanned(u);
      return `
        <tr>
          <td>${escapeHtml(u.username)}</td>
          <td class="id-cell">${escapeHtml(u.id)}</td>
          <td>
            <span class="badge ${banned ? "badge--banned" : "badge--ok"}">
              ${banned ? "Banned" : "Active"}
            </span>
          </td>
          <td class="col-actions">
            <button class="btn" data-action="ban" data-id="${escapeHtml(u.id)}">
              ${banned ? "Unban" : "Ban"}
            </button>
            <button class="btn btn--danger" data-action="delete" data-id="${escapeHtml(u.id)}" data-name="${escapeHtml(u.username)}">
              Delete
            </button>
          </td>
        </tr>`;
    })
    .join("");
}

async function loadUsers() {
  const body = document.getElementById("usersBody");
  body.innerHTML = `<tr><td colspan="4" class="empty-row">Loading…</td></tr>`;
  try {
    const data = await apiFetch("/getalluser");
    allUsers = data.users || [];
    renderUsers(allUsers);
  } catch (err) {
    body.innerHTML = `<tr><td colspan="4" class="empty-row">${escapeHtml(err.message)}</td></tr>`;
  }
}

document.getElementById("userSearch").addEventListener("input", (e) => {
  const q = e.target.value.trim().toLowerCase();
  const filtered = allUsers.filter(
    (u) =>
      (u.username || "").toLowerCase().includes(q) ||
      String(u.id || "").toLowerCase().includes(q)
  );
  renderUsers(filtered);
});

document.getElementById("usersBody").addEventListener("click", async (e) => {
  const btn = e.target.closest("button[data-action]");
  if (!btn) return;
  const id = btn.dataset.id;

  if (btn.dataset.action === "ban") {
    btn.disabled = true;
    try {
      const res = await apiFetch("/banuserorunban", { method: "PUT", params: { user_id: id } });
      showToast(res.message || "Updated");
      loadUsers();
    } catch (err) {
      showToast(err.message || "Could not update user", true);
      btn.disabled = false;
    }
  }

  if (btn.dataset.action === "delete") {
    const name = btn.dataset.name;
    if (!confirm(`Delete user "${name}"? This also removes their stored files and cannot be undone.`)) return;
    btn.disabled = true;
    try {
      const res = await apiFetch("/deleteuser", { method: "DELETE", params: { user_id: id } });
      showToast(res.message || "User deleted");
      loadUsers();
    } catch (err) {
      showToast(err.message || "Could not delete user", true);
      btn.disabled = false;
    }
  }
});

loadUsers();