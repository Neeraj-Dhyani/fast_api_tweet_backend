from peewee import CharField, TextField, DateTimeField, ForeignKeyField, IntegerField, JSONField
from database import BaseModel
import datetime

class User(BaseModel):
    username = CharField(unique=True, max_length=25)
    email = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    isban = CharField(default=False)
    bio = CharField(null=True)
    avatar = CharField(null=True)

    class Meta:
        table_name = "users"

class Following(BaseModel):
    from_user = ForeignKeyField(User, backref="following", on_delete="CASCADE")
    to_user = ForeignKeyField(User, backref="follower", on_delete="CASCADE")
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "follower"
        indexes =( 
            (("from_user", "to_user"), True)
        )

class Tweet(BaseModel):
    user = ForeignKeyField(User, backref="tweet", on_delete="CASCADE")
    content =  TextField()
    image_content = JSONField(null=True)
    support = IntegerField(default=0)
    created_at =  DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "Tweet"


class Support(BaseModel):
    user = ForeignKeyField(User, backref="tweet", on_delete="CASCADE")
    tweet = ForeignKeyField(Tweet, backref="tweet", on_delete="CASCADE")
    created_at =  DateTimeField(default=datetime.datetime.now)

    class Meta:
            table_name = "Support"
class Comment(BaseModel):
    user = ForeignKeyField(User, backref="Comment_user", on_delete="CASCADE")
    tweet = ForeignKeyField(Tweet, backref="tweet", on_delete="CASCADE")
    message = CharField()
    created_at =  DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "Comment"

class ReplyComment(BaseModel):
    User = ForeignKeyField(User, backref="Reply_user", on_delete="CASCADE")
    Comment = ForeignKeyField(Comment, backref="comment", on_delete="CASCADE")
    message = CharField()
    created_at =  DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "ReplyComment"
    