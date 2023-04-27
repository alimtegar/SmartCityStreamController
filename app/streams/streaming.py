from threading import Thread
import numpy as np
import time
import cv2
from supervision import Detections


from app.config import WANTED_CLASS_ID_LIST
from app.models import vehicle_detection_model, plate_detection_model, text_recognition_model
from app.utils import filter_detections, get_counter_area
from app.tracker import Tracker


class StreamingThread(Thread):
    def __init__(self, source, name, width, loop, counter_line, counter_area):
        Thread.__init__(self)
        self.name = name
        self.source = source
        self.width = width
        self.loop = loop
        self.counter_line = counter_line
        self.counter_area = counter_area

        self.capture = None  # type: cv2.VideoCapture
        self.current_frame = None
        self.status = "ready"

        self.should_stop = False
        self.should_flip = str(self.source).isnumeric()
        
        self.tracker = Tracker()

    def reset(self):
        self.status = "need_restart"

    def run(self):
        try:
            self.status = "starting"
            self.capture = cv2.VideoCapture(self.source)
            while True:
                time.sleep(0.02)
    
                # Loop the video
                if self.loop and self.capture.get(cv2.CAP_PROP_POS_FRAMES) == self.capture.get(cv2.CAP_PROP_FRAME_COUNT):
                    self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

                if self.status == "need_restart":
                    self.status = "starting"
                    self.capture = cv2.VideoCapture(self.source)
                    time.sleep(3)


                if self.should_stop:
                    self.should_stop = False
                    break

                success, frame = self.capture.read()
                if not success:
                    self.status = "failing"
                    time.sleep(1)
                    frame = np.zeros((240, 320, 3), np.uint8)
                    self.current_frame = cv2.imencode('.png', frame)[1].tobytes()

                else:
                    self.status = "running"
                    frame = image_resize(frame, width=self.width)

                    if self.should_flip:
                        frame = cv2.flip(frame, 1)

                    ## Assume here for Hard Processing
                    # Detect the vehicles on the frame
                    results = vehicle_detection_model(frame)[0]
                    vehicle_detections = Detections.from_yolov8(results).with_nms()
                    
                    # Filter the detections from unwanted classes
                    mask = np.array([class_id in WANTED_CLASS_ID_LIST for class_id in vehicle_detections.class_id], dtype=bool)
                    vehicle_detections = filter_detections(detections=vehicle_detections, mask=mask)
                    
                    # Track the vehicles
                    vehicle_detections = self.tracker.update(vehicle_detections)
                    for xyxy, confidence, class_id, tracker_id in vehicle_detections:
                        x1, y1, x2, y2 = xyxy.astype(np.int32)
                        dot_xy = [int(x2), int(y2)]

                        # Check if the vehicle is in `area1`
                        dot2area_dist = cv2.pointPolygonTest(np.array(self.counter_area, dtype=int), dot_xy, False)
                        is_in_area = dot2area_dist >= 0
                        
                        # Crop the frame with detected vehicle
                        # vehicle_image = frame[y1:y2, x1:x2] #.copy()

                        # Draw the bbox for the vehicle and draw a dot on the top-left of the bbox
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.circle(frame, dot_xy, 5, (255, 0, 255), -1)
                    
                    # Draw the counter area
                    cv2.polylines(img=frame, pts=[np.array(self.counter_area, dtype=int)], isClosed=True, color=(0, 0, 255), thickness=2)
                    
                    self.current_frame = cv2.imencode('.png', frame)[1].tobytes()
        finally:
            self.current_frame = None
            self.capture.release()


    def stream_frame(self):
        while self.current_frame:
            if self.status == "failing":
                time.sleep(1)
            else:
                time.sleep(0.02)

            yield self.current_frame


    def stop_frame(self):
        pass


    def stop(self):
        self.should_stop = True
        return True


# class VideoWriterThread(Thread):
#     def __init__(self, frame_generator, filename):
#         Thread.__init__(self)
#         self.frame_generator = frame_generator
#         self.should_stop = False

#         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#         self.video_writer = cv2.VideoWriter(filename, fourcc, 30, (640, 480))

#     def run(self) -> None:
#         try:
#             for frame in self.frame_generator():
#                 if self.should_stop: break

#                 self.video_writer.write(frame)
#         finally:
#             self.video_writer.release()
    
#     def end(self):
#         self.should_stop = True



def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
        pass

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized
