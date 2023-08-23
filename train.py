from ultralytics import YOLO

model = YOLO('yolov8m.pt')

model.train(data='/Users/madhuupadhyay/Documents/Whack-a-crypto/dataa.yaml', epochs=50, imgsz=640, patience = 10, device = 'mps', workers = 0,batch=4)
