"""
File Info object and config
"""
from pydantic import BaseModel, Field
from enum import Enum


def parse_s3_contents(file):
    """
    Parse s3 Contents
    """
    return FileInfo(**file)


class FileInfo(BaseModel):
    """
    A class to represent a file's information.
    ...
    Attributes
    ----------
    Key : str
        name of the file
    size : int
        size of the file
    metadata: dict
        key-value pair of metadata attached to file
    """

    Key: str = Field(alias="name")
    Size: int = Field(alias="size")
    Metadata: dict = Field(alias="metadata")

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

        allow_population_by_field_name = True

class FileReleaseType(Enum):
    """
    An enum class to represent a file's possible release type.
    """
    OUT_OF_CYCLE = "Out of Cycle"
    SAFETY_RELATED = "Safety Related"
    ENHANCEMENT_RELATED = "Enhancement Related"
    MANDATORY_UPDATE = "Mandatory Update"
