from typing import Union, List, Tuple

class Camera(object):
    id: int
    name: str
    source: Union[int, str]
    width: int
    loop: bool
    counter_line: List[Tuple[int, int]]

    def __init__(self, id, name, source, width, loop, counter_line) -> None:
        self.id = id
        self.name = name
        self.source = source
        self.width = width
        self.loop = loop
        self.counter_line = counter_line

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'source': self.source,
            'width': self.width,
            'loop': self.loop,
            'counter_line': self.counter_line
        }

    def __copy__(self):
        return type(self)(self.id, self.name, self.source, self.width, self.loop, self.counter_line)
        
