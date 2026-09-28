from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from peewee import IntegrityError
from models.model import User, Following
from models.schema import LoginUser, User_data, User_name, Bio_content
from helper.helper import save_the_file, update_the_file, delete_user_asset, remove_user_avatar
from dotenv import load_dotenv
from middleware.authentication import authentication
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
import os
from server import get_db


load_dotenv()

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


# ========================= 
#  REGISTER USER
# =========================

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user (
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    bio: str  | None = Form(None),
    file: UploadFile | None = File(None), 
    database=Depends(get_db) ):
    try:
        is_user = User.get_or_none(User.username == username)
        if is_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already Exits !"
            )

      
        avatar_url = save_the_file(file, username) if file  else  None

        if isinstance(avatar_url, dict):
              raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                             detail= avatar_url["detail"]
                         )

        salt  = bcrypt.gensalt()
        haspass = bcrypt.hashpw(password.encode("utf-8"), salt)

        str_haspass = haspass.decode("utf-8")

        user_db = User.create(username=username, password=str_haspass, email=email, avatar=avatar_url, bio= bio or None)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="User Created Successfully!"
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error!"
        )


# ========================= 
#  LOGIN 
# =========================

@router.post("/login" ,status_code=status.HTTP_200_OK)
def login(data:LoginUser, database=Depends(get_db)):
    try:
        username, password = data.username, data.password
        userByts = password.encode("utf-8")

        user = User.get_or_none(User.username == username)
        if not user:
            raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Username Not Found!" 
            )

        if user.isban == True:
              raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Your ban by admin"
                    )

        checkpassword = bcrypt.checkpw(userByts, user.password.encode("utf-8"))

        if not checkpassword:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your Password is Wrong!"
            )

        encode_jwt = jwt.encode(
                {
                    "data":{"username":user.username, "email":user.email},
                    "exp":datetime.now(timezone.utc) + timedelta(days=1)
                 },
                               
                    os.getenv("SECRET_JWT"), 
                    algorithm="HS256"
                )

        return {
            "Message":"Loggin Successfully!",
            "token" : encode_jwt
        }
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error!"
        )


# ========================= 
#  GET USER
# =========================

@router.get("/getuser", status_code=status.HTTP_200_OK)
def getuser(user=Depends(authentication)):
    return {
        "message":"User Fetched Successfully!",
        "user": user
    }

# ========================= 
#  UPDATE AND UPLOAD AVATAR
# =========================

@router.put("/uploadavatar")
def upload_avatar(file:UploadFile = File(...), user=Depends(authentication)):
    try:
        if user.avatar == None:
            avatar_url = ""
            avatar_url = save_the_file(file, user.username)
            raise HTTPException(
                status_code= status.HTTP_200_OK,
                detail="avatar uploaded Succeessfully!"
            )
        update_url = update_the_file(file, user.avatar)
        if isinstance(update_url, dict):
                      raise HTTPException(
                                    status_code=status.HTTP_400_BAD_REQUEST,
                                    detail= avatar_url["detail"]
                                 )
        return HTTPException(
             status_code=status.HTTP_200_OK,
             detail="Your Avatar Change Successfully!"
        )
    except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )


# ========================= 
#  UPDATE USER
# =========================

@router.put("/updateuser")
def update_user(data:User_data, user=Depends(authentication)):
    try:
        username, email = data.username, data.email

        if username and  email :
            selected_user = User.get_or_none(User.username == user.username)
            if not user:
                 raise HTTPException(
                      status_code=status.HTTP_404_NOT_FOUND,
                      detail="User Not Found"
                 )
            selected_user.username = username
            selected_user.email = email
            selected_user.save()
            return HTTPException(
                         status_code=status.HTTP_200_OK,
                         detail="Username and Email Update Successfully!"
                    )
        if username :
            selected_user = User.get_or_none(User.username == user.username)
            if not user:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="User Not Found"
                        )
            selected_user.username = username
            selected_user.save()
            return HTTPException(
                            status_code=status.HTTP_200_OK,
                            detail="Username Update Successfully!"
                            )
        if email :
                selected_user = User.get_or_none(User.username == user.username)
                if not user:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="User Not Found"
                            )
                selected_user.email = email
                selected_user.save()
                return HTTPException(
                            status_code=status.HTTP_200_OK,
                            detail="Email Update Successfully!"
                            )
        
             
    except ImportError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal Server Error!"
                )

# ========================= 
#  UPDATE USER
# =========================

@router.put("/updateuserbio")
def update_user_bio(content:Bio_content, user=Depends(authentication)):
    try:
            user = User.get_or_none(User.id == user.id)
            if not user:
                  raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found!"
                  )
            user.bio = content
            user.save()

            return {
                  "status":status.HTTP_200_OK,
                  "message":"Your bio  successfully updated!"
            }

    except ImportError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal Server Error!"
                )
            


# ========================= 
# REMOVE AVATAR 
# =========================

@router.delete("/removeavatar")
def remove_avatar(user=Depends(authentication)):
      try:
            user_data = User.get_or_none(User.username == user.username)
            if not user_data:
                   raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="User Not Found"
                        )
            if not user_data.avatar:
                    raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Avatar Not Found!"
                        )
            
            result = remove_user_avatar(user.avatar)
            if not result["success"]:
                print(result)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail= "Remove File Error!"
                   
            
                )
            user_data.avatar = None
            user_data.save()
            return {
                  "status":200,
                  "message":"Avatar Remove Successfully!"
            }
      except ImportError as err:
                print("error", err)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal Server Error!"
                )

# ========================= 
# DELETE_USER
# =========================

@router.delete("/deleteuser")
def delete_user(user=Depends(authentication)):
      try:
            
            user_data = User.get_or_none(User.username == user.username)
            if not user_data:
                        raise HTTPException(
                                    status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User Not Found"
                                    )
            
            result = delete_user_asset(user_data.username)

            if not result["success"]:
                   print(result)
                   raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail= "User Folder Not Deleted"

                        )

            user_data.delete_instance()
            return {
                  "status":status.HTTP_200_OK,
                  "message":"User Deleted Successfully"
            }

      except ImportError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal Server Error!"
                )


# ========================= 
# FOLLOWING USER
# =========================

@router.post("/following")
def create_following(data:User_name,user=Depends(authentication), database=Depends(get_db)):
    try:
        
        following_name = data.username
        follower_name = user.username
        isfollowing_user = User.get_or_none(User.username == following_name)
        if not isfollowing_user:
              raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User Not Found!"
              )
        following_user = Following.get_or_none(
                    Following.from_user == user.id & Following.to_user == isfollowing_user.id
                )
        if following_user:
              raise HTTPException(
                    status_code=status.Http_2
              )
        Following.create(from_user=user, to_user=isfollowing_user )
        return {
            "status":status.HTTP_200_OK,
            "message":f"{follower_name} Following user {following_name} Successfully!"
        }
    except ImportError :
          raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
          )

# ========================= 
# UNFOLLOW USER
# =========================

@router.delete("/unfollowing")
def unfollow(data:User_name,user=Depends(authentication), database=Depends(get_db)):
    try:
        
        following_name = data.username

       
        isfollowing_user = User.get_or_none(User.username == following_name)
        if not isfollowing_user:
              raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User Not Found!"
              )
        
        following_user = Following.get_or_none(
            Following.from_user == user.id & Following.to_user == isfollowing_user.id
        )

        if not following_user :
               raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="You are not following this user!"
                        )
        following_user.delete_instance()
        return {
            "status":status.HTTP_200_OK,
            "message":f" Unfollow user {following_name} Successfully!"
        }
    except ImportError :
          raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
          )

