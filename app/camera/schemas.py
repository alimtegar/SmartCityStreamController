from typing import Optional, Union
from pydantic import BaseModel


class CreateCamera(BaseModel):
    name: str
    source: Union[int, str]
    width: Optional[int] = 320


class EditCamera(BaseModel):
    name: Optional[str] = None
    source: Optional[Union[int, str]] = None


class CameraResponse(BaseModel):
    id: int
    name: str
    source: Union[int, str]
