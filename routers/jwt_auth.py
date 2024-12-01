# from uuid import uuid4
#
# from fastapi import status, HTTPException, Depends, APIRouter
# from fastapi.security import OAuth2PasswordRequestForm
#
# from models import db
# from schemas import UserOut, UserAuth, TokenSchema
# from utils import (
#     get_hashed_password,
#     create_access_token,
#     create_refresh_token,
#     verify_password
# )
#
# auth = APIRouter()
#
#
# @auth.post('/signup', summary="Create new user", response_model=UserOut)
# async def create_user(data: UserAuth):
#     user = db.get(data.email, None)
#     if user is not None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User with this email already exist"
#         )
#     user = {
#         'email': data.email,
#         'password': get_hashed_password(data.password),
#         'id': str(uuid4())
#     }
#     db[data.email] = user
#     return user
#
#
# @auth.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = db.get(form_data.username, None)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect email or password"
#         )
#
#     hashed_pass = user['password']
#     if not verify_password(form_data.password, hashed_pass):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect email or password"
#         )
#
#     return {
#         "access_token": create_access_token(user['email']),
#         "refresh_token": create_refresh_token(user['email']),
#     }
