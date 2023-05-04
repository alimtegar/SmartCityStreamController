from typing import Union, List, Tuple

class Camera(object):
    id: int
    # name: str
    source: Union[int, str]
    res: int
    loop: bool
    counter_line: List[Tuple[int, int]]

    def __init__(self, id, source, res, loop, counter_line) -> None:
        self.id = id
        # self.name = name
        self.source = source
        self.res = res
        self.loop = loop
        self.counter_line = counter_line

    def dict(self):
        return {
            'id': self.id,
            # 'name': self.name,
            'source': self.source,
            'res': self.res,
            'loop': self.loop,
            'counter_line': self.counter_line
        }

    def __copy__(self):
        return type(self)(self.id, self.source, self.res, self.loop, self.counter_line)
        
