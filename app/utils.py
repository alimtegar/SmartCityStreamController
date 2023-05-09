import re
import numpy as np
import cv2
import torch
import torch.nn.functional as F
from PIL import Image
from supervision import Detections
from torchvision import transforms

from app.config import IDX2CHAR, COUNTER_AREA_H, PLATE_CITY_MAP

def filter_detections(detections: Detections, mask: np.ndarray) -> Detections:
  return Detections(
    xyxy=detections.xyxy[mask],
    confidence=detections.confidence[mask],
    class_id=detections.class_id[mask],
    tracker_id=detections.tracker_id[mask]
    if detections.tracker_id is not None
    else None,
  )
  
def RGB(event, x, y, flags, param):
  if event == cv2.EVENT_MOUSEMOVE :  
    colorsBGR = [x, y]
    print(colorsBGR)
    
def upscale_image(img, new_w):
  # Get the aspect ratio of the original image
  h, w = img.shape[:2]
  aspect_ratio = w / h

  # Calculate the new height based on the aspect ratio
  new_h = int(new_w / aspect_ratio)

  # Upscale the image using the INTER_LINEAR interpolation method
  upscaled_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

  return upscaled_img

def draw_counter(img, counter, res=720):
  resRatio = res // 720
  x = 0
  y = 0
  fontScale = 5 if resRatio > 2 else 1
  p = 50 if fontScale > 1 else 10
  w = 458 if fontScale > 1 else 90 
  h = 52 if fontScale > 1 else 10
  w += (2 * p)
  h += (2 * p)
  
  cv2.rectangle(img=img, pt1=(x, y), pt2=(x+w, y+h), color=(0, 255, 0), thickness=-1)
  cv2.putText(img=img, text=f'Count: {len(counter.index):03}', org=(x+p, y+h-p), fontFace=1, fontScale=fontScale, color=(0, 0, 0), thickness=fontScale)

def get_counter_area(counter_line):
  line_start = counter_line[0]
  line_end = counter_line[1]
  
  return [
    (line_start[0], line_start[1] + COUNTER_AREA_H/2),
    (line_end[0], line_end[1] + COUNTER_AREA_H/2),
    (line_end[0], line_end[1] - COUNTER_AREA_H/2),
    (line_start[0], line_start[1] - COUNTER_AREA_H/2),
  ]

# Text Recognition Utils
def decode_text(labels):
  tokens = F.softmax(labels, 2).argmax(2)
  tokens = tokens.numpy().T
  plates = []
  for token in tokens:
      chars = [IDX2CHAR[idx] for idx in token]
      plate = ''.join(chars)
      plates.append(plate)
  return plates

def remove_duplicates(text):
  if len(text) > 1:
    letters = [text[0]] + [letter for idx, letter in enumerate(text[1:], start=1) if text[idx] != text[idx-1]]
  elif len(text) == 1:
    letters = [text[0]]
  else:
    return ''
  return ''.join(letters)

def correct_text(word):
  parts = word.split('-')
  parts = [remove_duplicates(part) for part in parts]
  corrected_text = ''.join(parts)
  return corrected_text

def recognize_text(np_image: np.ndarray, model):
  pil_image = Image.fromarray(np_image).convert('RGB')

  # Preprocess the image
  transform = transforms.Compose([
      transforms.Resize((256, 256)),
      transforms.ToTensor(),
      transforms.Normalize((0.5,), (0.5,))
  ])
  image = transform(pil_image)
  image = image.unsqueeze(0)

  # Perform inference
  with torch.no_grad():
    output = model(image)
    recognized_text = decode_text(output)
    recognized_text = correct_text(recognized_text[0])

  return recognized_text

def get_plate_city(plate_number: str):
  plate_city_code = re.match(r'[A-Za-z]{1,2}', plate_number)
  plate_city_code = plate_city_code.group() if plate_city_code else ''
                                                 # Default value, if `plate_city_code` doesn't exist in `PLATE_CITY_MAP`
  plate_city = PLATE_CITY_MAP.get(plate_city_code, '')
  return plate_city