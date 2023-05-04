from typing import Optional, Union, List, Tuple
from pydantic import BaseModel


class CreateCamera(BaseModel):
    # name: str
    source: Union[int, str]
    res: Optional[int] = 720
    loop: Optional[bool] = True
    counter_line: Optional[List[Tuple[int, int]]] = [(0,0), (0, 0)]

class EditCamera(BaseModel):
    # name: Optional[str] = None
    source: Optional[Union[int, str]] = None
    res: Optional[int] = None
    loop: Optional[bool] = None
    counter_line: Optional[List[Tuple[int, int]]] = [(0,0), (0, 0)]


class CameraResponse(BaseModel):
    id: int
    # name: str
    source: Union[int, str]
    res: int
    loop: bool
    counter_line: List[Tuple[int, int]]