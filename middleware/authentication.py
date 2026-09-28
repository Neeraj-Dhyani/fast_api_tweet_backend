from fastapi import Header, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.model import User
from dotenv import load_dotenv
import jwt 
import os


load_dotenv()
security = HTTPBearer()

def authentication(credentials : HTTPAuthorizationCredentials = Depends(security)):
        # if not authorization.startswith("Bearer "):
        #             raise HTTPException(
        #                 status_code=status.HTTP_401_UNAUTHORIZED,
        #                 detail="Invalid Authorization!"
        #             )
        
        token = credentials.credentials
        try:
            
            docoded = jwt.decode(token, os.getenv("SECRET_JWT"), algorithms=["HS256"])

            if docoded["admin"]:
                 raise HTTPException(
                      status_code=status.HTTP_403_FORBIDDEN,
                      detail="No user in database"
                 )
            
            user = User.get_or_none(User.username == docoded["data"]["username"])

            if not user:
                raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User Not Found!"
                    )

            return user
       
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

        
