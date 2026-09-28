"""
Server-rendered admin panel (Jinja templates) for the JWT admin API in
`admin.py`. This router only serves HTML shells + static assets — every
page fetches its data client-side from /api/v1/admin/* using the JWT
saved in localStorage after /adminlogin. Because of that, these page
routes are intentionally NOT protected by `adminAuthentication`: an
unauthenticated visitor just gets an empty shell that immediately
bounces to /admin/login (see static/js/api.js -> requireAuth()).

Mount alongside your existing admin API router, e.g. in main.py:

    from routers.admin import router as admin_api_router
    from routers.admin_panel import router as admin_panel_router

    app.include_router(admin_api_router)
    app.include_router(admin_panel_router)

Folder layout expected:

    templates/base.html, login.html, dashboard.html, users.html, tweets.html, comments.html   (project root)
    routers/static/css/admin.css                                                               (next to this file)
    routers/static/js/api.js, login.js, dashboard.js, users.js, tweets.js, comments.js
"""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# This file lives at routers/admin_panel.py.
# templates/ sits at the project root (sibling of routers/).
# static/ sits inside routers/ (sibling of this file).
PROJECT_ROOT = Path(__file__).resolve().parent




templates = Jinja2Templates(directory=str(PROJECT_ROOT / "templates"))
print(templates)
templates.env.cache = None


router = APIRouter(prefix="/admin", tags=["Admin Panel"])

# Serves /admin/static/css/admin.css, /admin/static/js/*.js, etc.
router.mount("/static_1", StaticFiles(directory=str(PROJECT_ROOT / "static")), name="admin_static")


@router.get("/")
def admin_root():
    return RedirectResponse(url="/admin/dashboard")


@router.get("/login")
def admin_login_page(request: Request):
    return templates.TemplateResponse(name="login.html", request=request, context={})


@router.get("/dashboard")
def admin_dashboard_page(request: Request):
    return templates.TemplateResponse(name="dashboard.html", request=request, context={})


@router.get("/users")
def admin_users_page(request: Request):
    return templates.TemplateResponse(name="users.html", request=request, context={})


@router.get("/tweets") 
def admin_tweets_page(request: Request):
    return templates.TemplateResponse(name="tweets.html", request=request, context={})


@router.get("/comments")
def admin_comments_page(request: Request):
    return templates.TemplateResponse(name="comments.html", request=request, context={})
