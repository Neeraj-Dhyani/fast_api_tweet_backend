from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from peewee import OperationalError
from database import db, get_db
from models.model import User, Following, Tweet, Support, Comment, ReplyComment
import os

import logging

from api.user_service import router as user_router
from api.tweet_service import router as tweet_router
from api.comment_service import router as comment_router
from api.admin_service import router as admin_router
from admin_panel import router as template_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifesspan(app:FastAPI):
    try:
        db.connect(reuse_if_open=True)
        db.create_tables([User, Following, Tweet, Support, Comment, ReplyComment])
        logger.info("Startup: Connected to the database successfully.")
        db.close()
    except OperationalError as e:
        logger.error(f"Startup: Failed to connect to database: {e}")
    yield

app = FastAPI(lifespan=lifesspan)


os.makedirs("uploads", exist_ok=True)

app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.get("/")
def read_root():
    return {"message":"Server OK!" }


@app.get("/health")
def check_health(database=Depends(get_db)):
    return {"status": "Database Connection Successfully!"}


app.include_router(user_router)
app.include_router(tweet_router)
app.include_router(comment_router)
app.include_router(admin_router)
app.include_router(template_router)