from peewee import MySQLDatabase, Model, OperationalError
from fastapi import HTTPException, status
from dotenv import load_dotenv
import pymysql
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
user = os.getenv("USER_NAME")
password = os.getenv("DATA_BASE_PASSWORD")
host  = "rcwmij.h.filess.io"
port = 3306
database = "MyDataBase_ratherfew"

db = MySQLDatabase(database, user=user, password=password, host=host, port=port)

class BaseModel(Model):
    class Meta:
        database = db

def get_db():
    
    try:
        db.connect(reuse_if_open=True)
        yield db

    except OperationalError as e:
    
        logger.error(f"Request failed - Database connection error: {e}")
        
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database server is currently unavailable."
        )
    finally:
        if not db.is_closed():
            db.close()