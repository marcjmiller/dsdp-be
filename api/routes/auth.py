from fastapi import APIRouter

router = APIRouter()

@router.get("/user/roles", name="auth:getUserRoles")
def user_roles():
    return "Hello world! 5.1"
    