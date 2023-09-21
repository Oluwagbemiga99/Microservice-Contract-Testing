from typing import  List
from fastapi import APIRouter, Query, Security
from starlette import status
from starlette.responses import JSONResponse
from database.Users import Users
from middleware.Key import get_api_key
from schemas.Requests import GetUser
from schemas.User import User

router = APIRouter()



@router.get("/users", response_model=List[User])
async def get_users(
    api_key: str = Security(get_api_key),
    offset: int = Query(default=0),
    limit: int = Query(default=10),
    
) -> JSONResponse:
    return Users.getUsers(offset,limit)


@router.get("/user")
async def get_one_user(
    query: GetUser,
    api_key: str = Security(get_api_key)
) -> JSONResponse:
    
    user = Users.getUserByEmail(query.email)
    if user is not None:
        return user
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'msg':'User not found'})


@router.post("/user",status_code=status.HTTP_201_CREATED)
async def create_user(
    user: User,
    api_key: str = Security(get_api_key)
) -> JSONResponse:
    if(Users.getUserByEmail(user.email)):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'msg':'Cannot create user!'})
    Users.addUser(user)
    return user

@router.patch("/user")
async def update_user(
    email: str,
    user: User,
    api_key: str = Security(get_api_key)
) -> JSONResponse:
    if(not Users.getUserByEmail(user.email)):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'msg':'Cannot update user!'})
    Users.updateUser(email=email,user=user)
    return user


@router.delete("/user")
async def delete_user(
    query: GetUser,
    api_key: str = Security(get_api_key)
) -> JSONResponse:
    Users.removeUserByEmail(query.email)
    return ""