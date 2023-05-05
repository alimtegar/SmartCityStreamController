# import torch
import torch.nn as nn
# from ultralytics import YOLO
from torchvision.models import resnet18

# from app.config import VEHICLE_DETECTION_MODEL_PATH, PLATE_DETECTION_MODEL_PATH, TEXT_RECOGNITION_MODEL_PATH, VOCABULARY

resnet = resnet18(weights=None)

class CRNN(nn.Module):
  def __init__(self, num_chars, rnn_hidden_size=256, dropout=0.1):
    super(CRNN, self).__init__()
    self.num_chars = num_chars
    self.rnn_hidden_size = rnn_hidden_size
    self.dropout = dropout
    
    # Get resnet18 without the last 3 layers
    resnet_modules = list(resnet.children())[:-3]
    self.cnn_p1 = nn.Sequential(*resnet_modules)
    
    # Add custom layers
    self.cnn_p2 = nn.Sequential(
        nn.Conv2d(
            in_channels=256,
            out_channels=256,
            kernel_size=(3,6),
            stride=1,
            padding=1),
        nn.BatchNorm2d(num_features=256),
        nn.ReLU(inplace=True)
    )
    self.linear1 = nn.Linear(4*1024, 256)
    
    # RNN
    self.rnn1 = nn.GRU(
        input_size=rnn_hidden_size,
        hidden_size=rnn_hidden_size,
        bidirectional=True,
        batch_first=True
    )
    self.rnn2 = nn.GRU(
        input_size=rnn_hidden_size,
        hidden_size=rnn_hidden_size,
        bidirectional=True,
        batch_first=True
    )
    self.linear2 = nn.Linear(self.rnn_hidden_size*2, num_chars)
    
  def forward(self, x):
    x = self.cnn_p1(x)
    x = self.cnn_p2(x)
    x = x.permute(0,3,1,2)

    batch_size = x.size(0)
    T = x.size(1)
    x = x.view(batch_size, T, -1)
    x = self.linear1(x)

    x, hidden = self.rnn1(x)
    feature_size = x.size(2)
    x = x[:, :, :feature_size//2] + x[:, :, feature_size//2:]

    x, hidden = self.rnn2(x)
    x = self.linear2(x)
    x = x.permute(1,0,2)

    return x

# vehicle_detection_model = YOLO(VEHICLE_DETECTION_MODEL_PATH)
# vehicle_detection_model.fuse()

# plate_detection_model = YOLO(PLATE_DETECTION_MODEL_PATH)
# plate_detection_model.fuse()

# text_recognition_model = CRNN(num_chars=len(VOCABULARY))
# text_recognition_model.load_state_dict(torch.load(TEXT_RECOGNITION_MODEL_PATH, map_location=torch.device('cpu')))