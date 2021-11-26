# Python
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List


# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

app = FastAPI()


# Models ////////////////////////////////////////////////////////////////////////////////////////////////////////////////


class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(..., example='felipot@gmail.nz')


class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Felipe'
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Bucherenick'
    )
    birth_date: Optional[date] = Field(default=None,)


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        example='holasoyfelipe'
    )


class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        example='holasoyfelipereg'
    )


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)


# Path Operations ///////////////////////////////////////////////////////////////////////////////////////////////////

# USERS =====================================================================================

# Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    # Singup  
    ## This path operation register a user  
    ### Parameters:  
      - #### Request Body:  
          - **user:** *UserRegister*  
    ### Returns a JSON with the basic user information:  
      - **user_id:** *UUID*  
      - **email:** *EmailStr*  
      - **first_name:** *str*  
      - **last_name:** *str*  
      - **birth_date:** *Optional[date]*            
    """
    with open('users.json', 'r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user


# Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login(user_login: UserLogin = Body(...)):
    """
    # Login
    ## This path operation login a user  
    ### Parameters:  
      - #### Request Body:  
          - **user:** *UserLogin*  
    ### Returns a JSON with the basic user information:  
      - **user_id:** *UUID*  
      - **email:** *EmailStr*  
      - **first_name:** *str*  
      - **last_name:** *str*  
      - **birth_date:** *Optional[date]*            
    """
    with open('users.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
        users_list = list(results)
        user_login_dict = user_login.dict()
        for user in users_list:
            if user_login_dict['email'] == user['email']:
                if user_login_dict['password'] == user['password']:
                    return user


# Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    # Show all users  
    ## This path operation shows all users in the app.  
    ### Parameters:  
      -  
    ### Returns a JSON list with all the users in the app, with the following keys:  
      - **user_id:** *UUID*  
      - **email:** *EmailStr*  
      - **first_name:** *str*  
      - **last_name:** *str*  
      - **birth_date:** *Optional[date]*            
    """
    with open('users.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
        return results


# Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user(user_id: UUID = Field(...)):
    """
    # Show a user  
    ## This path operation shows a user in the app.  
    ### Parameters:  
      - #### Path parameter:  
          - **user_id:** *UUID*  
    ### Returns a JSON with the basic user information:  
      - **user_id:** *UUID*  
      - **email:** *EmailStr*  
      - **first_name:** *str*  
      - **last_name:** *str*  
      - **birth_date:** *Optional[date]*            
    """
    with open('users.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
        users_list = list(results)
        for user in users_list:
            if user['user_id'] == str(user_id):
                return user


# Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user(user_id: UUID = Field(...)):
    """
    # Delete a user  
    ## This path operation delete a user in the app.  
    ### Parameters:  
       - #### Path parameter:  
          - **user_id**: *UUID*  
    ### Returns a JSON with a delete user information with the next structure:  
       - **user_id:** *UUID*  
       - **email:** *EmailStr*  
       - **first_name:** *str*  
       - **last_name:** *str*  
       - **birth_date:** *Optional[date]*         
     """

    with open('users.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
        users_list = list(results)
        f.close()
    for user in users_list:
        if user['user_id'] == str(user_id):
            user_index = users_list.index(user)
            deleted_user = users_list.pop(user_index)
    with open('users.json', 'w', encoding='utf-8') as f:
        f.write(str(users_list))
    return deleted_user


# Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user(user: User = Body(...)):
    """
    # Update a user
    ## This path operation update a user in the app.  
    ### Parameters:  
       - #### Request Body:
          - **user**: *User*  
    ### Return a JSON with the original User info. and a second with the updated info with the next structure:  
       - **user_id:** *UUID*  
       - **email:** *EmailStr*  
       - **first_name:** *str*  
       - **last_name:** *str*  
       - **birth_date:** *Optional[date]*      
     """
    with open('users.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
        users_list = list(results)
        f.close()
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['email'] = str(user_dict['email'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
    for original_user in users_list:
        if str(original_user['user_id']) == user_dict['user_id']:
            user_index = users_list.index(original_user)
            old_user = users_list.pop(user_index)
            users_list.insert(user_index, user_dict)
    with open('users.json', 'w', encoding='utf-8') as f:
        f.write(str(users_list))
    return old_user

    # TWEETS =================================================================================

    # Show  all tweets


@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def home():
    """
    # Home  
    ## This path operation shows all tweets in the app.  
    ### Parameters:  
      -  
    ### Returns a JSON list with all the tweets in the app, with the following keys:  
      - **tweet_id:** *UUID*  
      - **content:** *str*  
      - **created_at:** *datetime*  
      - **updated_at:** *Optional[datetime]*  
      - **by:** *User*                        
    """
    with open('tweets.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
        return results


# Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    # Post a tweet  
    ## This path operation post a tweet in the app.  
    ### Parameters:  
      - #### Request Body:  
          - **tweet:** *Tweet*  
    ### Returns a JSON with the basic tweet information:  
      - **tweet_id:** *UUID*  
      - **content:** *str*  
      - **created_at:** *datetime*  
      - **updated_at:** *Optional[datetime]*  
      - **by:** *User*            
    """
    with open('tweets.json', 'r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet_dict["tweet_id"])
        tweet_dict['created_at'] = str(tweet_dict["created_at"])
        tweet_dict['updated_at'] = str(tweet_dict["updated_at"])
        tweet_dict['by']['user_id'] = str(tweet_dict["by"]['user_id'])
        tweet_dict['by']['birth_date'] = str(tweet_dict["by"]['birth_date'])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet


# Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet(tweet_id: UUID = Field(...)):
    """
    ### Show a tweet  
    ## This path operation show a tweet.
    ### Parameters:  
      - #### Path parameter:  
        - **tweet_id**: *UUID*
    ### Returns a JSON with a tweet information with the next structure:  
      - **tweet_id**: *UUID*  
      - **content**: *str*  
      - **created_at**: *datetime*  
      - **updated_at**: *Optional[datetime]*
      - **by**: *User*     
     """
    with open('tweets.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
        tweets_list = list(results)
        for tweet in tweets_list:
            if tweet['tweet_id'] == str(tweet_id):
                return tweet


# Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(tweet_id: UUID = Field(...)):
    """
    ### Delete a tweet  
    ## This path operation delete a tweet.
    ### Parameters:  
      - #### Path parameter:  
        - **tweet_id**: *UUID*
    ### Returns a JSON with a deleted tweet information with the next structure:  
      - **tweet_id**: *UUID*  
      - **content**: *str*  
      - **created_at**: *datetime*  
      - **updated_at**: *Optional[datetime]*
      - **by**: *User*     
     """
    with open('tweets.json', 'r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        f.close()
    tweets_list = list(results)
    for tweet in tweets_list:
        if tweet['tweet_id'] == str(tweet_id):
            tweet_index = tweets_list.index(tweet)
    removed_tweet = tweets_list.pop(tweet_index)
    new_results = str(tweets_list)
    with open('tweets.json', 'w', encoding='utf-8') as f:
        f.write(new_results)
    return removed_tweet


# Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet(tweet: Tweet = Body(...)):
    """
    # Update a tweet
    ## This path operation update a tweet in the app.  
    ### Parameters:  
       - #### Request Body:
          - **tweet**: *Tweet*  
    ### Return a JSON with the original Tweet info. and a second with the updated info with the next structure:  
       - **tweet_id**: *UUID*  
       - **content**: *str*  
       - **created_at**: *datetime*  
       - **updated_at**: *Optional[datetime]*
       - **by**: *User*          
     """
    with open('tweets.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
        tweets_list = list(results)
        f.close()
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet_dict['tweet_id'])
        tweet_dict['created_at'] = str(tweet_dict['created_at'])
        tweet_dict['updated_at'] = str(tweet_dict['updated_at'])
        tweet_dict['by']['user_id'] = str(tweet_dict["by"]['user_id'])
        tweet_dict['by']['birth_date'] = str(tweet_dict["by"]['birth_date'])
    for original_tweet in tweets_list:
        if str(original_tweet['tweet_id']) == tweet_dict['tweet_id']:
            tweet_index = tweets_list.index(original_tweet)
            old_tweet = tweets_list.pop(tweet_index)
            tweets_list.insert(tweet_index, tweet_dict)
    with open('tweets.json', 'w', encoding='utf-8') as f:
        f.write(str(tweets_list))
    return old_tweet
