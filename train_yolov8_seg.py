
from ultralytics import YOLO

# Load a YOLOv8-seg nano model (best for CPU/low resources)
model = YOLO('yolov8n-seg.pt')

# Train the model with improved settings
model.train(
    data='biscuit_crack.yaml',
    epochs=50,            # 50 epochs as requested
    imgsz=640,            # Image size (default 640)
    device='cpu',         # Use 'cuda' if have a GPU
    lr0=0.001,            # Lower initial learning rate
    val=True,             # Run validation after each epoch
    save=True,            # Save checkpoints and results
    project='runs/segment',
    name='biscuit_yolov8n_seg',
)

# After training, check the folder runs/segment/biscuit_yolov8n_seg/val_pred/
# It contains images with predicted crack masks for each validation image after each epoch.
# Open these images to visually inspect how well the model is learning to segment cracks.
