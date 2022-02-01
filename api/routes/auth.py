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
        user_info = UserInfo(
            **decoded,
            is_admin=("/Platform One/gvsc/IL2/roles/admin" in decoded['group-full'])
        )
    except (DecodeError, Exception) as exception:
        logging.info("%s, Auth:%s", authorization, exception)
        raise exception
    return user_info
