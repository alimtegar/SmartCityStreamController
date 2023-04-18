from typing import Union

class Camera(object):
    id: int
    name: str
    source: Union[int, str]
    width: int
    loop: bool

    def __init__(self, id, name, source, width, loop) -> None:
        self.id = id
        self.name = name
        self.source = source
        self.width = width
        self.loop = loop

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'source': self.source,
            'width': self.width,
            'loop': self.loop,
        }

    def __copy__(self):
        return type(self)(self.id, self.name, self.source, self.width, self.loop)
        
