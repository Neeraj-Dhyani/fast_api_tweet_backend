let allComments = [];

// FKs come back as plain ids once the endpoints use .dicts() (see README).
function userLabel(c) {
  const u = c.user;
  if (u && typeof u === "object") return u.username ?? u.id ?? "—";
  return u ?? "—";
}

function tweetLabel(c) {
  const t = c.tweet;
  if (t && typeof t === "object") return t.id ?? "—";
  return t ?? "—";
}

function renderComments(comments) {
  const body = document.getElementById("commentsBody");
  if (!comments.length) {
    body.innerHTML = `<tr><td colspan="4" class="empty-row">No comments found.</td></tr>`;
    return;
  }
  body.innerHTML = comments
    .map(
      (c) => `
        <tr>
          <td class="id-cell">${escapeHtml(c.id)}</td>
          <td>${escapeHtml(userLabel(c))}</td>
          <td class="id-cell">${escapeHtml(tweetLabel(c))}</td>
          <td class="content-cell" title="${escapeHtml(c.message)}">${escapeHtml(c.message)}</td>
        </tr>`
    )
    .join("");
}

async function loadComments() {
  const body = document.getElementById("commentsBody");
  body.innerHTML = `<tr><td colspan="4" class="empty-row">Loading…</td></tr>`;
  try {
    const data = await apiFetch("/getallcomment");
    allComments = data.comments || [];
    renderComments(allComments);
    document.getElementById("commentsTitle").textContent = "All comments";
  } catch (err) {
    body.innerHTML = `<tr><td colspan="4" class="empty-row">${escapeHtml(err.message)}</td></tr>`;
  }
}

document.getElementById("commentSearch").addEventListener("input", (e) => {
  const q = e.target.value.trim().toLowerCase();
  const filtered = allComments.filter(
    (c) =>
      String(c.id || "").toLowerCase().includes(q) ||
      (c.message || "").toLowerCase().includes(q)
  );
  renderComments(filtered);
});

document.getElementById("lookupUserBtn").addEventListener("click", async () => {
  const note = document.getElementById("lookupNote");
  const userId = document.getElementById("lookupUserId").value.trim();
  if (!userId) return;
  note.classList.remove("error");
  note.textContent = "Looking up user's comments…";
  try {
    const data = await apiFetch("/getcommentbyuser", { params: { user_id: userId } });
    allComments = data.user_tweet || [];
    renderComments(allComments);
    document.getElementById("commentsTitle").textContent = `Comments by user ${userId}`;
    note.textContent = `Showing ${allComments.length} comment(s) from user ${userId}. Reload to see all comments again.`;
  } catch (err) {
    note.classList.add("error");
    note.textContent = err.message || "No comments for this user";
    renderComments([]);
  }
});

loadComments();