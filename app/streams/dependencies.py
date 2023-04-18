import logging
from typing import Dict, Union

from app.streams.streaming import StreamingThread


log = logging.getLogger(__name__)
streamings: Dict[str, StreamingThread] = dict()

def add_stream(name: str, source: Union[int, str], width: int, loop: bool):
    print("Adding stream:", name, source, width, loop)
    thread = StreamingThread(source, name, width, loop)
    streamings.update({name: thread})
    thread.start()


def reset_stream(name: str, source: Union[int, str], width: int, loop: bool):
    print("Resetting stream:", name, source, width, loop)
    thread = streamings.get(name)

    thread.source = source
    thread.width = width
    thread.loop = loop

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
