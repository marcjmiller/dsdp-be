import logging
from typing import Optional
from fastapi import APIRouter, Header
from jwt import decode
from api.models.user_info import UserInfo

auth_router = APIRouter()


@auth_router.get("/whoami", name="auth:getUserRoles")
def who_am_i(authorization: Optional[str] = Header(None)) -> UserInfo:
    if authorization is None:
        return UserInfo(name="Nobody",is_admin=False)

    try:
        encoded_token = authorization.split(" ")[1]
        decoded = decode(encoded_token, options={"verify_signature": False})
        user_info = UserInfo(
            **decoded,
            is_admin=("/Platform One/gvsc/IL2/roles/admin" in decoded['group-full'])
        )
    except Exception as exception:
        logging.info("Auth: %s\n Except: %s", authorization, exception)
        raise exception
    return user_info
