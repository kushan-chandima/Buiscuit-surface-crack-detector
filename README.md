# Biscuit Surface Crack Detector

This project uses YOLOv8-seg for real-time biscuit crack detection and segmentation. It features a user-friendly PyQt5 interface for live monitoring and automated crack identification.

![Interface Preview](ui_preview.png)

## Features
- **Real-time segmentation**: Accurately outlines cracks on moving biscuits.
- **Dual Engine Support**: Run with PyTorch (recommended) or ONNX Runtime.
- **Visual Feedback**: Direct red-highlighted overlays for clear crack identification.

## Detection Results
Below are sample results showing the segmentation accuracy on various biscuit types:

| Original Image | Detection Result |
| :---: | :---: |
| ![Original 1](samples/sample_1.jpg) | ![Detected 1](samples/sample_1_detected.jpg) |
| ![Original 2](samples/sample_2.jpg) | ![Detected 2](samples/sample_2_detected.jpg) |
| ![Original 3](samples/sample_3.jpg) | ![Detected 3](samples/sample_3_detected.jpg) |

## Setup

1. Create and activate the virtual environment:
   ```bash
   python -m venv env-biscuits-crack
   # On Windows PowerShell:
   .\env-biscuits-crack\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Real-Time UI (Recommended)
```bash
python app/main.py
```
- Select your camera from the dropdown.
- Click **Start** to begin live detection.
- Cracks will be highlighted in **red** on the video feed.

### Command Line Inference
```python
from ultralytics import YOLO

model = YOLO('runs/segment/biscuit_yolov8n_seg/weights/best.pt')
results = model.predict('path/to/image.jpg', save=True)
# Results saved to runs/segment/predict/
```

## Training
1. Organize your dataset as described in `biscuit_crack.yaml`.
2. Run the training script:
   ```bash
   python train_yolov8_seg.py
   ```

## Troubleshooting
- **DLL Errors**: If you encounter DLL issues with PyTorch on Windows, ensure you have the [latest Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) installed.
- **Performance**: For systems without a GPU, use the ONNX version with `python app/main_onnx.py`.

## Contributing
Pull requests are welcome! For major changes, please open an issue first.

## License
MIT
