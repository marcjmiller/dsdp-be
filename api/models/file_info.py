from pydantic import BaseModel, Field


class FileInfo(BaseModel):
    """
    A class to represent a file's information.
    ...
    Attributes
    ----------
    name : str
        name of the file
    size : int
        size of the file
    """
    Key: str = Field( alias='name')
    Size: int = Field( alias='size')
    class Config:
        """
        Configuration class of FileDto
        ...
        Attributes
        ----------
        allow_population_by_field_name : bool
            whether the class may have the fields
            populated by the fields name in addition
            to it's alias
        """
        allow_population_by_field_name=True
