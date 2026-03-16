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


## Real-Time UI Usage

You can run the user-friendly UI for live crack detection using either the PyTorch (Ultralytics) or ONNX version:

### PyTorch/Ultralytics UI (Recommended)
```
python app/main.py
```
- Select your camera from the dropdown.
- Click **Start** to begin live detection. Cracks will be highlighted in red on the video feed.
- Click **Stop** to end detection.
   - Uses your trained model at `runs/segment/biscuit_yolov8n_seg/weights/best.pt` by default. Update the path in `app/main.py` if needed.

### ONNX Runtime UI (No PyTorch Required)
```
python app/main_onnx.py
```
- Uses the exported ONNX model at `runs/segment/runs/segment/biscuit_yolov8n_seg/weights/best.onnx`.
- Useful if you cannot use PyTorch (e.g., DLL issues), but mask overlay may require tuning for perfect alignment.

## Troubleshooting
- If you get DLL errors with PyTorch, ensure you have the latest Microsoft Visual C++ Redistributable (x64) installed and only one version present.
- If using ONNX UI, mask overlay may need adjustment depending on your camera resolution and model export settings.
- For missing packages, activate your environment and run `pip install -r requirements.txt`.
- For more help, open an issue or contact the maintainer.

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
- `app/main.py`: PyQt5 real-time UI for live crack detection

## License
MIT
