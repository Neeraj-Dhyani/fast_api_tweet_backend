# Control Room — Admin Panel

A Jinja2-templated admin panel for your existing `/api/v1/admin/*` FastAPI
routes. Pages are server-rendered shells; all data comes from your API via
`fetch`, using the JWT from `/adminlogin` stored in `localStorage`.

## Files

```
routers/admin_panel.py     # New router: serves the HTML pages + static files
templates/                 # base.html, login.html, dashboard.html, users.html, tweets.html, comments.html
static/css/admin.css       # Styling
static/js/api.js           # Shared fetch/auth helper (loaded on every page)
static/js/login.js, dashboard.js, users.js, tweets.js, comments.js
```

## Install

```bash
pip install jinja2 python-multipart
```

## Wire it up

Put `admin_panel.py` next to your existing `admin.py` router, and copy
`templates/` and `static/` to your project root (or adjust the paths in
`admin_panel.py`'s `BASE_DIR` if you keep them elsewhere). Then in your
`main.py`:

```python
from routers.admin import router as admin_api_router      # your existing API
from routers.admin_panel import router as admin_panel_router  # new UI

app.include_router(admin_api_router)
app.include_router(admin_panel_router)
```

Visit `/admin/login`, sign in with the admin name/password from your
`.env` (`ADMIN`, `PASSWORD`), and you'll land on `/admin/dashboard`.

## Two things in the pasted API worth fixing before this will fully work

1. **`deleteuser` route is missing its leading slash.**
   ```python
   @router.delete("deleteuser")   # should be @router.delete("/deleteuser")
   ```
   As written, that path won't register the way the others do, so the
   panel's delete-user button will 404 until this is corrected.

2. **`getalluser` / `getalltweet` / `getallcomment` / `gettweetbyid` return
   raw Peewee model instances** (`Tweet.select()`, not `.dicts()`),
   while `gettweetsbyuser` and `getcommentbyuser` already correctly call
   `.dicts()`. FastAPI can't JSON-serialize a bare Peewee model, so those
   four endpoints will likely raise a 500 at request time. The fix is the
   same pattern already used elsewhere in the file:
   ```python
   tweets = list(Tweet.select().dicts())
   users = list(User.select().dicts())
   comments = list(Comment.select().dicts())
   tweet = Tweet.get_or_none(Tweet.id == tweet_id)
   ...
   "tweet": model_to_dict(tweet)  # or Tweet.select().where(...).dicts().get()
   ```
   The panel expects plain JSON objects with fields like `id`, `username`,
   `isban`, `user`, and `content` — adjust the field names in
   `static/js/*.js` (`tweetText()`, `userLabel()`, etc.) if your actual
   column names differ.

## What each page does

- **Login** — posts to `/adminlogin`, stores the JWT + admin name in `localStorage`.
- **Overview** — pulls all three lists once to show counts + banned users.
- **Users** — lists all users, client-side filter, ban/unban toggle, delete (with confirmation).
- **Tweets** — lookup by tweet ID or user ID, full list with filter, delete.
- **Comments** — lookup by user ID, full list with filter (read-only — no delete endpoint was provided).

Every page redirects to `/admin/login` if there's no token, and any `401`
from the API clears the session and redirects too.
