# Biscuit Surface Crack Detector

This project uses YOLOv8-seg for real-time biscuit crack detection and segmentation.

## Setup

1. Create and activate the virtual environment:
   ```
   python -m venv env-biscuits-crack
   # On Windows PowerShell:
   .\env-biscuits-crack\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Training

1. Organize your dataset as described in `biscuit_crack.yaml`.
2. Run the training script:
   ```
   python train_yolov8_seg.py
   ```

## Inference and UI

### Inference (Prediction)

After training, you can use your best model to predict cracks on new images or video streams.

#### Predict on Images
```
from ultralytics import YOLO

model = YOLO('runs/segment/biscuit_yolov8n_seg/weights/best.pt')
results = model.predict('path/to/image.jpg', save=True)
```
- This will save prediction images with crack masks in the `runs/segment/predict/` folder.

#### Predict on Video (Live Camera)
```
model.predict(source=0, show=True)  # 0 = default webcam
```
- Use `source=1`, `2`, etc. for other connected cameras.

### Real-Time UI (Planned)
- A PyQt5-based UI will allow you to select the video source, view live predictions, and highlight cracks in red.
- (To be implemented)

## Troubleshooting
- If training does not improve, check your dataset and annotations.
- For missing packages, activate your environment and run `pip install -r requirements.txt`.
- For more help, open an issue or contact the maintainer.

## Contributing
Pull requests are welcome! Please open an issue first to discuss major changes.

## Files
- `biscuit_crack.yaml`: Dataset config
- `train_yolov8_seg.py`: Training script
- `env-biscuits-crack/`: Virtual environment (do not commit)

## License
MIT
