let allTweets = [];

// FKs come back as plain ids once /getalltweet etc. use .dicts() (see README).
function userLabel(t) {
  const u = t.user;
  if (u && typeof u === "object") return u.username ?? u.id ?? "—";
  return u ?? "—";
}

function renderTweets(tweets) {
  const body = document.getElementById("tweetsBody");
  if (!tweets.length) {
    body.innerHTML = `<tr><td colspan="5" class="empty-row">No tweets found.</td></tr>`;
    return;
  }
  body.innerHTML = tweets
    .map(
      (t) => `
        <tr>
          <td class="id-cell">${escapeHtml(t.id)}</td>
          <td>${escapeHtml(userLabel(t))}</td>
          <td class="content-cell" title="${escapeHtml(t.content)}">${escapeHtml(t.content)}</td>
          <td>${escapeHtml(t.support ?? 0)}</td>
          <td class="col-actions">
            <button class="btn btn--danger" data-action="delete" data-id="${escapeHtml(t.id)}">Delete</button>
          </td>
        </tr>`
    )
    .join("");
}

async function loadTweets() {
  const body = document.getElementById("tweetsBody");
  body.innerHTML = `<tr><td colspan="5" class="empty-row">Loading…</td></tr>`;
  try {
    const data = await apiFetch("/getalltweet");
    allTweets = data.tweets || [];
    renderTweets(allTweets);
  } catch (err) {
    body.innerHTML = `<tr><td colspan="5" class="empty-row">${escapeHtml(err.message)}</td></tr>`;
  }
}

document.getElementById("tweetSearch").addEventListener("input", (e) => {
  const q = e.target.value.trim().toLowerCase();
  const filtered = allTweets.filter(
    (t) =>
      String(t.id || "").toLowerCase().includes(q) ||
      (t.content || "").toLowerCase().includes(q)
  );
  renderTweets(filtered);
});

document.getElementById("tweetsBody").addEventListener("click", async (e) => {
  const btn = e.target.closest("button[data-action='delete']");
  if (!btn) return;
  if (!confirm("Delete this tweet? This cannot be undone.")) return;
  btn.disabled = true;
  try {
    const res = await apiFetch("/deleteusertweet", { method: "DELETE", params: { tweet_id: btn.dataset.id } });
    showToast(res.message || "Tweet deleted");
    loadTweets();
  } catch (err) {
    showToast(err.message || "Could not delete tweet", true);
    btn.disabled = false;
  }
});

// ---- Lookup by tweet id ----
document.getElementById("lookupTweetBtn").addEventListener("click", async () => {
  const note = document.getElementById("lookupNote");
  const id = document.getElementById("lookupTweetId").value.trim();
  if (!id) return;
  note.classList.remove("error");
  note.textContent = "Looking up tweet…";
  try {
    const data = await apiFetch("/gettweetbyid", { params: { tweet_id: id } });
    allTweets = [data.tweet];
    renderTweets(allTweets);
    note.textContent = `Showing tweet ${id}. Clear the search box above or reload to see all tweets.`;
  } catch (err) {
    note.classList.add("error");
    note.textContent = err.message || "Tweet not found";
  }
});

// ---- Lookup by user id ----
document.getElementById("lookupUserBtn").addEventListener("click", async () => {
  const note = document.getElementById("lookupNote");
  const userId = document.getElementById("lookupUserId").value.trim();
  if (!userId) return;
  note.classList.remove("error");
  note.textContent = "Looking up user's tweets…";
  try {
    const data = await apiFetch("/gettweetsbyuser", { params: { user_id: userId } });
    allTweets = data.user_tweet || [];
    renderTweets(allTweets);
    note.textContent = `Showing ${allTweets.length} tweet(s) from user ${userId}. Reload to see all tweets again.`;
  } catch (err) {
    note.classList.add("error");
    note.textContent = err.message || "No tweets for this user";
    renderTweets([]);
  }
});

loadTweets();