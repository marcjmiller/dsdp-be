"""
Auth endpoints
"""
from typing import List, Optional
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, Header, HTTPException
from jwt import decode
from jwt.exceptions import DecodeError
from app.models.user_info import AdminInfo, UserInfo
from app.api.deps import get_s3_client
from app.core.config import get_settings


settings = get_settings()

router = APIRouter()


def __parse_admins(admin):
    return admin.get("Key")[7::]


def __retrieve_admins(s3):
    objects = s3.list_objects(Bucket=settings.MINIO_BUCKET_NAME, Prefix="admins")
    return [__parse_admins(obj) for obj in objects.get("Contents", [])]


def __check_if_admin(token, admins):
    if "/Platform One/gvsc/IL2/roles/admin" in token["group-full"]:
        return True
    if token["preferred_username"] in admins:
        return True
    return False


@router.get("/whoami", name="auth:whoami")
def who_am_i(authorization: Optional[str] = Header(None), s3=Depends(get_s3_client)) -> UserInfo:
    """Takes in the auth header and returns a UserInfo object"""
    if authorization is None:
        return UserInfo(name="Nobody", is_admin=True, preferred_username="nobody.ctr")

    try:
        encoded_token = authorization.split(" ")[1]
        decoded = decode(encoded_token, options={"verify_signature": False})
        admins = __retrieve_admins(s3)
        user_info = UserInfo(
            **decoded,
            is_admin=__check_if_admin(decoded, admins),
        )
    except DecodeError:
        raise HTTPException(status_code=500, detail="Not a valid token")
    return user_info


@router.get("/admins", name="auth:admins")
async def list_admins(s3=Depends(get_s3_client)) -> List[str]:
    return __retrieve_admins(s3)


@router.post("/admins", name="auth:admins")
def add_admin(admin_info: AdminInfo, s3=Depends(get_s3_client)) -> List[str]:
    try:
        s3.put_object(
            Bucket=settings.MINIO_BUCKET_NAME,
            Key="admins/" + admin_info.username,
        )
        return __retrieve_admins(s3)
    except ClientError as error:
        raise HTTPException(
            status_code=500, detail=f"Something went wrong with s3:\n\t{error}"
        )
