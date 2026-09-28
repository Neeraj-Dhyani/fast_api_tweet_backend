(async function loadStats() {
  try {
    const [usersRes, tweetsRes, commentsRes] = await Promise.all([
      apiFetch("/getalluser"),
      apiFetch("/getalltweet"),
      apiFetch("/getallcomment"),
    ]);

    const users = usersRes.users || [];
    const tweets = tweetsRes.tweets || [];
    const comments = commentsRes.comments || [];
    const banned = users.filter(isBanned).length;

    document.getElementById("statUsers").textContent = users.length;
    document.getElementById("statTweets").textContent = tweets.length;
    document.getElementById("statComments").textContent = comments.length;
    document.getElementById("statBanned").textContent = banned;
  } catch (err) {
    showToast(err.message || "Could not load stats", true);
  }
})();