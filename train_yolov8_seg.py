from ultralytics import YOLO

# Load a YOLOv8-seg nano model (best for CPU/low resources)
model = YOLO('yolov8n-seg.pt')

# Train the model
model.train(
    data='biscuit_crack.yaml',
    epochs=50,           # You can adjust epochs as needed
    imgsz=640,           # Image size (default 640)
    device='cpu'         # Use 'cuda' if you have a GPU
)
