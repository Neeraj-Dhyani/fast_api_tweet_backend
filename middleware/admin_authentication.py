from fastapi import Header, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import jwt 
import os


load_dotenv()
security = HTTPBearer()

def adminAuthentication(credentials:HTTPAuthorizationCredentials=Depends(security)):
    try:
        token = credentials.credentials

        decode = jwt.decode(token, os.getenv("SECRET_JWT"), algorithms=["HS256"])
        if decode["admin"] != os.getenv("ADMIN"):
              raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User Not Found!"
                    )
         
        return{ 
            "admin":decode["admin"]
         }
     
    except jwt.ExpiredSignatureError:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired!"
        )

    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token!"
        )