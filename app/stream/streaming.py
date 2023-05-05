from threading import Thread
import numpy as np
import time
import cv2
import torch
import pandas as pd
from datetime import datetime
from supervision import Detections


from app.config import WANTED_CLASS_ID_LIST, CLASS_NAME_MAP
# from app.models import vehicle_detection_model, plate_detection_model, text_recognition_model
from app.utils import filter_detections, draw_counter, upscale_image, recognize_text, get_plate_city
from app.tracker import Tracker
from app.vehicle.schemas import VehicleSchema
from app.vehicle.dependencies import add_vehicle_to_db


class StreamingThread(Thread):
    def __init__(self, source, name, res, loop, counter_line, counter_area, vehicle_detection_model, plate_detection_model, text_recognition_model):
        Thread.__init__(self)
        self.name = name
        self.source = source
        self.res = res
        self.loop = loop
        self.counter_line = counter_line
        self.counter_area = counter_area
        self.vehicle_detection_model = vehicle_detection_model
        self.plate_detection_model = plate_detection_model
        self.text_recognition_model = text_recognition_model

        self.capture = None  # type: cv2.VideoCapture
        self.current_frame = None
        self.status = "ready"

        self.should_stop = False
        self.should_flip = str(self.source).isnumeric()
        
        self.tracker = Tracker()
        self.counter = pd.DataFrame(columns=['tracker_id', 'plate_number'])

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
                    frame = image_resize(frame, width=self.res)

                    if self.should_flip:
                        frame = cv2.flip(frame, 1)

                    ## Assume here for Hard Processing
                    # Detect the vehicles on the frame
                    results = self.vehicle_detection_model(frame)[0]
                    vehicle_detections = Detections.from_yolov8(results).with_nms()
                    
                    # print(f'detections on {self.name} = ', len(vehicle_detections))
                    
                    # Filter the detections from unwanted classes
                    mask = np.array([class_id in WANTED_CLASS_ID_LIST for class_id in vehicle_detections.class_id], dtype=bool)
                    vehicle_detections = filter_detections(detections=vehicle_detections, mask=mask)
                    
                    if len(vehicle_detections):
                        # Track the vehicles
                        vehicle_detections = self.tracker.update(vehicle_detections)
                        for xyxy, confidence, class_id, tracker_id in vehicle_detections:
                            x1, y1, x2, y2 = xyxy.astype(np.int32)
                            dot_xy = [int(x2), int(y2)]

                            # Check if the vehicle is in `area1`
                            dot2area_dist = cv2.pointPolygonTest(np.array(self.counter_area, dtype=int), dot_xy, False)
                            is_in_area = dot2area_dist >= 0
                            
                            # Crop the frame with detected vehicle
                            vehicle_image = frame[y1:y2, x1:x2] #.copy()

                            # Draw the bbox for the vehicle and draw a dot on the top-left of the bbox
                            cv2.rectangle(img=frame, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=1)
                            cv2.circle(img=frame, center=dot_xy, radius=2, color=(255, 0, 255), thickness=-1)
                            
                            if is_in_area and not tracker_id in self.counter['tracker_id'].values:
                                # Detect the plate of the vehicle
                                plate_detections = self.plate_detection_model.predict(vehicle_image)[0]

                                # Process the plate detection if any
                                if (len(plate_detections) > 0):
                                    # Get the highest confidence plate detection
                                    max_plate_detection_boxes = plate_detections.boxes[torch.argmax(plate_detections.boxes.conf)]
                                    max_plate_detection_xyxy = max_plate_detection_boxes.xyxy[0]
                                    max_plate_detection_conf = max_plate_detection_boxes.conf[0]
                                    
                                    x1, y1, x2, y2 = map(int, max_plate_detection_xyxy[:4])

                                    # If plate detection confidence bigger than the threshold, show the detection
                                    PLATE_DETECTION_CONF_THRESHOLD = 0.8
                                    if max_plate_detection_conf >= PLATE_DETECTION_CONF_THRESHOLD:
                                        plate_image = vehicle_image[y1:y2, x1:x2]
                                        plate_image = upscale_image(img=plate_image, new_w=360)
                                        
                                        # Recognize the text of the plate number
                                        plate_number = recognize_text(plate_image, self.text_recognition_model)
                                        
                            #             # Add vehicle to DB
                            #             vehicle = VehicleSchema(
                            #                 timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            #                 vehicleType=CLASS_NAME_MAP[class_id],
                            #                 plateNumber=plate_number,
                            #                 plateCity=get_plate_city(plate_number),
                            #             )
                            #             add_vehicle_to_db(vehicle)
                                        
                                        # Count the vehicles
                                        self.counter.loc[len(self.counter.index)] = [tracker_id, plate_number] 
                                        self.counter.drop_duplicates(subset='tracker_id', keep='last', ignore_index=True, inplace=True)
                                        self.counter.drop_duplicates(subset='plate_number', keep='last', ignore_index=True, inplace=True)
                    
                    draw_counter(img=frame, counter=self.counter, res=self.res)
                    cv2.polylines(img=frame, pts=[np.array(self.counter_area, dtype=int)], isClosed=True, color=(0, 0, 255), thickness=1)
                    
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
