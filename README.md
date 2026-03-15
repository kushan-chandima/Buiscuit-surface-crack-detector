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

- (To be added) Real-time video inference and UI for crack visualization.

## Files
- `biscuit_crack.yaml`: Dataset config
- `train_yolov8_seg.py`: Training script
- `env-biscuits-crack/`: Virtual environment (do not commit)

## License
MIT
