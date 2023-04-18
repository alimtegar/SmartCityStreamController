from typing import Union

class Camera(object):
    id: int
    name: str
    source: Union[int, str]
    width: int

    def __init__(self, id, name, source, width) -> None:
        self.id = id
        self.name = name
        self.source = source
        self.width = width

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'source': self.source,
            'width': self.width
        }

    def __copy__(self):
        return type(self)(self.id, self.name, self.source, self.width)
        
