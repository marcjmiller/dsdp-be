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
        decoded = decode(encoded_token, options={"verify_signature": False})
        logging.info(f"encoded: {encoded_token}, decoded: {decoded}")
        user_info = UserInfo(
            **decoded
        )

    except (DecodeError, Exception) as exception:
        logging.info(f"{exception}, Auth:{authorization}")
        raise exception
    return user_info
