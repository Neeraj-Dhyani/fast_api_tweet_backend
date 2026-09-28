from fastapi import Header, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os 

load_dotenv()
security = HTTPBearer()
def api_key_auth(credentials:HTTPAuthorizationCredentials=Depends(security)):
    try:
          api_key  = credentials.credentials
          if not api_key:
                raise HTTPException(
                      status_code=status.HTTP_401_UNAUTHORIZED,
                      detail="No API key!"
                )
          if os.getenv("API_KEY") != api_key:
                raise HTTPException(
                      status_code=status.HTTP_401_UNAUTHORIZED,
                      detail="API key is wrong!"
                )
          return
    except Exception :
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired!"
        )