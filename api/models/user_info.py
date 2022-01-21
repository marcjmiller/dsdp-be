from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    name: str
    # groups: List[str] = Field(..., alias="group-full")
