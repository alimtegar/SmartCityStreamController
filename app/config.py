VEHICLE_DETECTION_MODEL_PATH = 'yolov8n.pt'
PLATE_DETECTION_MODEL_PATH = './model_weights/plate_detection_model_nano.pt'
TEXT_RECOGNITION_MODEL_PATH = './model_weights/text_recognition_model.pt'
VIDEO_PATH = 'vehicle-traffic-2.webm'

# Class IDs of Interest
WANTED_CLASS_ID_LIST = [
    1, # bicycle
    2, # car
    3, # motorcycle
    5, # bus
    7, # truck
]

# LINE_START = (540, 2210)
LINE_START = (540, 2110)
LINE_END = (3834, 1370)

# Text Recognition Configs
VOCABULARY = [
    '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z'
]
IDX2CHAR = {k: v for k, v in enumerate(VOCABULARY, start=0)}
CHAR2IDX = {v: k for k, v in IDX2CHAR.items()}