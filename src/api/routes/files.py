from fastapi import APIRouter


router = APIRouter()


@router.get("", name="files:hello")
async def hello():
  return {"data": "Hello, World!"}
