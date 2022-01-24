from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    name: str
    is_admin: bool = Field( alias='isAdmin')
    # groups: List[str] = Field(..., alias="group-full")
    class Config:
        allow_population_by_field_name=True
