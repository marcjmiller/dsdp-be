from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    """
    A class to represent a user's identity information.
    ...
    Attributes
    ----------
    name : str
        name of the user
    is_admin : bool
        Whether the user is an admin or not
    """
    name: str
    is_admin: bool = Field( alias='isAdmin')
    class Config:
        """
        Configuration class of UserInfo
        ...
        Attributes
        ----------
        allow_population_by_field_name : bool
            whether the class may have the fields 
            populated by the fields name in addition 
            to it's alias
        """
        allow_population_by_field_name=True
