"""
Auth endpoints
"""
from typing import Optional
from fastapi import APIRouter, Header, HTTPException
from jwt import decode
from jwt.exceptions import DecodeError
from app.models.user_info import UserInfo

router = APIRouter()


@router.get("/whoami", name="auth:whoami")
def who_am_i(authorization: Optional[str] = Header(None)) -> UserInfo:
    """Takes in the auth header and returns a UserInfo object"""
    if authorization is None:
        return UserInfo(name="Nobody", is_admin=True)

    try:
        encoded_token = authorization.split(" ")[1]
        decoded = decode(encoded_token, options={"verify_signature": False})
        user_info = UserInfo(
            **decoded,
            is_admin=("/Platform One/gvsc/IL2/roles/admin" in decoded["group-full"]),
        )
    except DecodeError:
        raise HTTPException(status_code=500, detail="Not a valid token")
    return user_info
