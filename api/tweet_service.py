from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from peewee import IntegrityError
from typing import List, Annotated
from models.model import Tweet, User, Support
from middleware.authentication import authentication
from helper.helper import save_multiple_file, delete_user_post
from database import get_db
from datetime import datetime


router = APIRouter(
    prefix="/api/v1/tweet",
    tags=["Tweet"]
)

@router.post("/posttweet")
def create_tweet(
    content: str = Form(...),
    image_files: Annotated[List[UploadFile] | None, File(description="select your images")] = None,
    user = Depends(authentication), 
    database = Depends(get_db)):

    time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    try:

        image_urls =  save_multiple_file(image_files, user.username, time)
        if not image_urls["success"]:
            print("error:",image_urls["error"])
            print("mode:", image_urls["mode"])
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=image_urls["error"]
            )

        # print(image_urls["images"])
        
        Tweet.create(user=user, content=content, image_content=image_urls["images"] or None, )
        return {
            "status":status.HTTP_200_OK,
            "message":"Post Uploaded Successfully!"
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error!"
            )

@router.delete("/deletetweet")
def delete_tweet(tweet_id, user=Depends(authentication)):
    try:
        user = User.get_or_none(User.username == user.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )
        tweet = Tweet.get_or_none(Tweet.id == tweet_id)
        if not tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )
        
        if tweet.user.id != user.id:
             raise HTTPException(
                  status_code=status.HTTP_403_FORBIDDEN,
                  detail="You cannot delete this tweet!"
             )
        result = delete_user_post(tweet.image_content)
        if not result["success"]:
                    # print("error:",result["error"])
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                        detail=result["error"]
                    )
        tweet.delete_instance()
        return{
            "status":status.HTTP_200_OK,
            "message":"Tweet Delete Successfully!"
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error!"
            )



@router.post("/support")
def toggel_support(post_id=str, user=Depends(authentication), database=Depends(get_db)):
     try:
        tweet = Tweet.get_or_none(Tweet.id == post_id)
        support = Support.get_or_none((Support.user == user) & (Support.tweet == tweet))
        print(support)
        if support:
             tweet.support -= 1
             tweet.save
             support.delete_instance()

             return{
                "status":status.HTTP_200_OK,
                "message":"Unsupported!"
             }
             
        if not tweet:
             raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Tweet not found!"
                        )
        tweet.support += 1
        tweet.save()
        Support.create(user=user, tweet=tweet)

        return{
            "status":status.HTTP_200_OK,
            "message":"Post Suppoted!"
        }     
        
     except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error!"
            )
     