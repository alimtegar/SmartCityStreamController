import logging
from typing import Dict, Union, List, Tuple

from app.streams.streaming import StreamingThread
from app.utils import get_counter_area


log = logging.getLogger(__name__)
streamings: Dict[str, StreamingThread] = dict()

def add_stream(name: str, source: Union[int, str], width: int, loop: bool, counter_line: List[Tuple[int, int]]):
    print("Adding stream:", name, source, width, loop, counter_line)
    counter_area = get_counter_area(counter_line)
    thread = StreamingThread(source, name, width, loop, counter_line, counter_area)
    streamings.update({name: thread})
    thread.start()


def reset_stream(name: str, source: Union[int, str], width: int, loop: bool, counter_line: List[Tuple[int, int]]):
    thread = streamings.get(name)
    if source: thread.source = source
    if width: thread.width = width
    if loop: thread.loop = loop
    if counter_line: 
        thread.counter_line = counter_line
        thread.counter_area = get_counter_area(counter_line)
    print("Resetting stream:", name, thread.source, thread.width, thread.loop, thread.counter_line)

    thread.reset()

    # thread = streamings.pop(name)
    # if thread.is_alive():
    #     thread.stop()
    # add_stream(name, source)


def remove_stream(name: str):
    print("Removing stream:", name)
    thread = streamings.pop(name)
    if thread.is_alive():
        thread.stop()


def stop_all_streamings():
    for stream in streamings.values():
        stream.stop()

    for stream in streamings.values():
        stream.join()
