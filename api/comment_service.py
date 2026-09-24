from fastapi import APIRouter, Depends, HTTPException, status
from peewee import IntegrityError
from models.model import Tweet, User, Comment, ReplyComment
from middleware.authentication import authentication
from database import get_db
from models.schema import Message

router = APIRouter(
    prefix="/api/v1/comment",
    tags=["Comment"]
)

@router.post("/commenttweet")
def comment_tweet(tweet_id:str, comment_conten=Message, user=Depends(authentication), database=Depends(get_db)):
    try:
        tweet = Tweet.get_or_none(Tweet.id == tweet_id)
        if not tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tweet Not Found!"
            )
        Comment.create(tweet=tweet, user=user, message=comment_conten)
        return{
            "status":status.HTTP_200_OK,
            "message":"Comment successfully!"
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error!"
            )

@router.put("/editcomment")
def comment_tweet(comment_id:str, update_conten=Message, user=Depends(authentication)):
    try:
        comment = Comment.get_or_none(Comment.id == comment_id)
        if not Comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tweet Not Found!"
            )
        if comment.user.id != user.id:
                     raise HTTPException(
                          status_code=status.HTTP_403_FORBIDDEN,
                          detail="You cannot edit this comment"
                     )
        comment.message = update_conten
        comment.save()
        return{
            "status":status.HTTP_200_OK,
            "message":"Comment  updated successfully!"
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error!"
            )

@router.delete("/deletecomment")
def delete_comment(comment_id:str, user=Depends(authentication)):
    try:
        comment=Comment.get_or_none(Comment.id == comment_id)
        if not comment:
             raise HTTPException(
                  status_code=status.HTTP_404_NOT_FOUND,
                  detail="Comment not found! " 
             )
        if comment.user.id != user.id:
             raise HTTPException(
                  status_code=status.HTTP_403_FORBIDDEN,
                  detail="You cannot delete this comment"
             )
        comment.delete_instance()
        return {
             "status":status.HTTP_200_OK,
             "message":"Comment deleted successfully!"
        }
    except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
                )

@router.post("/replycomment")
def reply_comment(comment_id:str, message=Message, user=Depends(authentication), database=Depends(get_db)):
     try:
          comment =  Comment.get_or_none(Tweet.id == comment_id)
          if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found! " 
                    )
          ReplyComment.create(user=user, comment=comment, message=message)
          return{
               "status":status.HTTP_200_OK,
               "message":"Reply comment successfully!"
          }
     except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
                )

@router.delete("/deletereplycomment")
def delete_tweet(reply_comment_id:str, user=Depends(authentication)):
    try:
        reply_comment=ReplyComment.get_or_none(ReplyComment.id == reply_comment_id )
        if not reply_comment:
             raise HTTPException(
                  status_code=status.HTTP_404_NOT_FOUND,
                  detail="Comment not found! " 
             )
        if reply_comment.user.id == user.id:
             raise HTTPException(
                  status_code=status.HTTP_403_FORBIDDEN,
                  detail="You cannot delete this comment"
             )
        ReplyComment.delete_instance()
        return {
             "status":status.HTTP_200_OK,
             "message":"Reply comment deleted successfully!"
        }
    except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
                )
