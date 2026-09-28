from fastapi import APIRouter, Depends, HTTPException, status
from models.model  import User, Tweet, Comment, ReplyComment
from middleware.API_key_auth import api_key_auth

router = APIRouter(prefix="/api/v1", tags=["App_API"])


@router.get("/all_user")
def get_all_user(api_key=Depends(api_key_auth)):
    try:
        all_user = list(User.select().dicts)

        return{
             "status":status.HTTP_200_OK,
             "users":all_user
        }
    except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )

@router.get("/getiuserbyid")
def get_user_by_id(user_id:str, api_key=Depends(api_key_auth)):
    try:
              user = User.get_or_none(User.id == user_id)
              if not user:
                    raise HTTPException(
                          status_code=status.HTTP_404_NOT_FOUND,
                          detail="User not found!"
                    )
              return{
                   "status":status.HTTP_200_OK,
                   "users":user
              }
    except ImportError:
                  raise HTTPException(
                      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail="Internal Server Error!"
                  )

    
@router.get("/getalltweet")
def get_all_tweet(api_key=Depends(api_key_auth)):
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
def get_tweet_by_id(tweet_id:str, api_key=Depends(api_key_auth)):
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
def get_tweets_by_user(user_id:str, api_key=Depends(api_key_auth)):
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



@router.get("/getallcomment")
def get_all_comment(api_key=Depends(api_key_auth)):
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
def get_tweets_by_user(user_id:str, api_key=(api_key_auth)):
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


@router.get("/replycomment")
def get_all_reply_comment(api_key=Depends(api_key_auth)):
     try:
         comments = list(ReplyComment.select())
         return{
              "status":status.HTTP_200_OK,
              "replycomment": comments
         }


     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )
     
@router.get("/getallreplybycomment")
def get_all_reply_by_comment(comment_id:str, api_key=Depends(api_key_auth)):
      try:
            reply = list(ReplyComment.select().where(ReplyComment.Comment == comment_id).dicts())
            if not reply:
                  raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No Reply!"
                  )
            return{
                  "status":status.HTTP_200_OK,
                  "reply":reply
            }
      except ImportError:
                  raise HTTPException(
                      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail="Internal Server Error!"
                  )

@router.get("/getcommentbyuser")
def get_comment_by_user(comment_id:str, api_key=(api_key_auth)):
     try:
          reaply_comment = list(ReplyComment.select().where(ReplyComment.Comment == Comment.id).dicts())
          if not reaply_comment:
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This user has no tweet"
               )
          return {
               "status":status.HTTP_200_OK,
               "reply":reaply_comment
          }
     except ImportError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error!"
            )
