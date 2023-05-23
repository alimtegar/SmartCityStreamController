import logging
import torch
from typing import Dict, Union, List, Tuple
from ultralytics import YOLO

from app.config import VEHICLE_DETECTION_MODEL_PATH, PLATE_DETECTION_MODEL_PATH, TEXT_RECOGNITION_MODEL_PATH, TEXT_RECOGNITION_CHARSET_TEST, DEVICE
# from app.models import CRNN
from app.stream.streaming import StreamingThread
from app.utils import get_counter_area
from app.strhub.models.utils import load_from_checkpoint

log = logging.getLogger(__name__)
streamings: Dict[str, StreamingThread] = dict()

def add_stream(name: str, source: Union[int, str], res: int, loop: bool, counter_line: List[Tuple[int, int]]):
    print("Adding stream:", name, source, res, loop, counter_line)
    
    # Get the area where the counter is located
    counter_area = get_counter_area(counter_line)
    
    # Initialize and load the YOLO model for vehicle detection
    vehicle_detection_model = YOLO(VEHICLE_DETECTION_MODEL_PATH)
    vehicle_detection_model.fuse()
    
    # Initialize and load the YOLO model for license plate detection
    plate_detection_model = YOLO(PLATE_DETECTION_MODEL_PATH)
    plate_detection_model.fuse()
    
    # Initialize and load the model for text recognition
    # text_recognition_model = CRNN(num_chars=len(VOCABULARY))
    # text_recognition_model.load_state_dict(torch.load(TEXT_RECOGNITION_MODEL_PATH, map_location=torch.device('cpu')))
    text_recognition_model = load_from_checkpoint(TEXT_RECOGNITION_MODEL_PATH, charset_test=TEXT_RECOGNITION_CHARSET_TEST).eval().to(DEVICE)
    
    thread = StreamingThread(
        source, 
        name, 
        res, 
        loop, 
        counter_line, 
        counter_area, 
        vehicle_detection_model,
        plate_detection_model,
        text_recognition_model,
    )
    streamings.update({name: thread})
    thread.start()


def reset_stream(name: str, source: Union[int, str], res: int, loop: bool, counter_line: List[Tuple[int, int]]):
    thread = streamings.get(name)
    if source: thread.source = source
    if res: thread.res = res
    if loop: thread.loop = loop
    if counter_line: 
        thread.counter_line = counter_line
        thread.counter_area = get_counter_area(counter_line)
    print("Resetting stream:", name, thread.source, thread.res, thread.loop, thread.counter_line)

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
