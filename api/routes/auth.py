import logging
from typing import Optional
from fastapi import APIRouter, Header
from jwt import DecodeError, decode
from api.models.user_info import UserInfo

auth_router = APIRouter()


@auth_router.get("/whoami", name="auth:getUserRoles")
def who_am_i(authorization: Optional[str] = Header(None)) -> UserInfo:
    if authorization is None:
        return {}

    try:
        encoded_token = authorization.split(" ")[1]
        user_info = UserInfo(
            **decode(encoded_token, options={"verify_signature": False})
        )

    except (DecodeError, Exception) as exception:
        logging.info(f"{exception}, Auth:{authorization}")
        raise exception
    return user_info
