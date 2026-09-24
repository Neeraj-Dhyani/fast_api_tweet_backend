from fastapi import APIRouter, Depends, HTTPException, status
from middleware.admin_authentication import adminAuthentication
from datetime import datetime, timedelta, timezone
from models.model  import User, Tweet, Comment, ReplyComment
from helper.helper import delete_user_asset 
from models.schema import LoginAdmin

from dotenv import load_dotenv
import os
import jwt

load_dotenv()

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"]
)

@router.post("/adminlogin")
def login_admin(admindata:LoginAdmin):
    try:
        adminname, password = admindata.adminname, admindata.password
        if adminname !=  os.getenv("ADMIN"):
            raise HTTPException(
                 status_code=status.HTTP_401_UNAUTHORIZED,
                 detail="Admin name is Wrong!"

            )
        if password != os.getenv("PASSWORD"):
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password is Wrong!"
             )

        encode_jwt = jwt.encode({"admin":adminname , "exp":datetime.now(timezone.utc) + timedelta(days=1)},  
                                os.getenv("SECRET_JWT"), algorithm="HS256")

        return {
             "status":status.HTTP_200_OK,
             "message":"Login Successfully!",
             "token":encode_jwt
        }
    except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )

@router.get("/getadmin")
def get_admin(admin=Depends(adminAuthentication)):
     try:
          return admin
     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )

@router.get("/getalluser")
def get_all_user(admin=Depends(adminAuthentication)):
     try:
          users = list(User.select())
          return{
            "status":status.HTTP_200_OK,
            #    "users":[
            #         user.__data__
            #         for user in users
            #    ]
            "users":users
          }
     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )

     
@router.get("/getalltweet")
def get_all_tweet(admin=Depends(adminAuthentication)):
     try:
         tweets = list(Tweet.select())
         return{
              "status":status.HTTP_200_OK,
              "tweets": tweets
         }

     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )
     

@router.get("/gettweetbyid")
def get_tweet_by_id(tweet_id:str, admin=Depends(adminAuthentication)):
     try:
          tweet = Tweet.get_or_none(Tweet.id == tweet_id)
          if not tweet:
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="tweet not found!"
               )
          return{
               "status":status.HTTP_200_OK,
               "tweet":tweet
          }
     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )


     
@router.get("/gettweetsbyuser")
def get_tweets_by_user(user_id:str, admin=Depends(adminAuthentication)):
     try:
          tweet_by_user = list(Tweet.select().where(Tweet.user == user_id).dicts())
          if not tweet_by_user:
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This user has no tweet"
               )
          return {
               "status":status.HTTP_200_OK,
               "user_tweet":tweet_by_user
          }
     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )

@router.delete("/deleteusertweet")
def delete_user_tweet(tweet_id:str, admin=Depends(adminAuthentication)):
     try:
          tweet = Tweet.get_or_none(Tweet.id == tweet_id)
          if not tweet:
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tweet not found!" 
               )
          tweet.delete_instance()
          return{ 
               "status":status.HTTP_200_OK,
               "message":"Tweet deleted successfully!"
          }
     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )

     
@router.get("/getallcomment")
def get_all_comment(admin=Depends(adminAuthentication)):
     try:
         comments = list(Comment.select())
         return{
              "status":status.HTTP_200_OK,
              "comments": comments
         }


     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )

@router.get("/getcommentbyuser")
def get_tweets_by_user(user_id:str, admin=Depends(adminAuthentication)):
     try:
          tweet_by_user = list(Comment.select().where(Comment.user == user_id).dicts())
          if not tweet_by_user:
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This user has no tweet"
               )
          return {
               "status":status.HTTP_200_OK,
               "user_tweet":tweet_by_user
          }
     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )

          
@router.put("/banuserorunban")
def ban_user_or_unban_user(user_id:str, admin=Depends(adminAuthentication)):
     try:
         user = User.get_or_none(User.id == user_id)
         if not user:
              raise HTTPException(
                   status_code=status.HTTP_404_NOT_FOUND,
                   detail="User not found!"
              )
         if user.isban == True:
              user.isban = False
              user.save()
              return {
                   "status":status.HTTP_200_OK,
                   "message":"User unban successfully!"
              }
         user.isban = True
         user.save()
         return{
              "status":status.HTTP_200_OK,
              "message":"User ban successfully!"
         }
     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )

@router.delete("/deleteuser")
def delete_user(user_id:str, admin=Depends(adminAuthentication)):
     try:
          user = User.get_or_none(User.id == user_id)
          if not user:
               raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found!"
                    )
          result = delete_user_asset(user.username)
          
          if not result["success"]:
                print(result)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail= "User Folder Not Deleted"
          
                )
     
          user.delete_instance()
          return{
               "status":status.HTTP_200_OK,
               "message":"User deleted successfully!"
          }
     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )
               