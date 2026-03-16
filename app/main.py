import torch
from ultralytics import YOLO
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QWidget, QHBoxLayout, QFrame
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class CrackDetectorUI(QMainWindow):
    def __init__(self, model_path):
        super().__init__()
        self.setWindowTitle('Biscuit Crack Detector Pro')
        self.setMinimumSize(1100, 800)
        
        # Initialize YOLO
        self.model = YOLO(model_path)
        self.capture = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.device = 'cpu'

        # Apply Global Stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QWidget {
                color: #E0E0E0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QFrame#ControlPanel {
                background-color: #1E1E1E;
                border-right: 1px solid #333333;
                min-width: 250px;
                max-width: 300px;
            }
            QFrame#VideoContainer {
                background-color: #000000;
                border: 2px solid #333333;
                border-radius: 8px;
            }
            QLabel#HeaderTitle {
                font-size: 24px;
                font-weight: bold;
                color: #00ADB5;
                margin-bottom: 10px;
            }
            QLabel#StatusLabel {
                font-style: italic;
                color: #AAAAAA;
                padding: 10px;
                background-color: #252525;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #333333;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton#StartBtn {
                background-color: #00ADB5;
                color: #FFFFFF;
            }
            QPushButton#StartBtn:hover {
                background-color: #00F5FF;
            }
            QPushButton#StopBtn {
                background-color: #FF2E63;
                color: #FFFFFF;
            }
            QPushButton#StopBtn:hover {
                background-color: #FF5E89;
            }
            QComboBox {
                background-color: #252525;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QLabel#ResultIndicator {
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border-radius: 4px;
                background-color: #333333;
                color: #FFFFFF;
                qproperty-alignment: AlignCenter;
            }
        """)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Sidebar / Control Panel ---
        sidebar = QFrame()
        sidebar.setObjectName("ControlPanel")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(15)

        title = QLabel("CRACK\nDETECTOR")
        title.setObjectName("HeaderTitle")
        sidebar_layout.addWidget(title)
        
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #333333; max-height: 1px;")
        sidebar_layout.addWidget(sep)

        sidebar_layout.addWidget(QLabel("Camera Source:"))
        self.source_combo = QComboBox()
        sidebar_layout.addWidget(self.source_combo)

        self.start_button = QPushButton('START DETECTION')
        self.start_button.setObjectName("StartBtn")
        self.start_button.clicked.connect(self.start_detection)
        sidebar_layout.addWidget(self.start_button)

        self.stop_button = QPushButton('STOP')
        self.stop_button.setObjectName("StopBtn")
        self.stop_button.clicked.connect(self.stop_detection)
        sidebar_layout.addWidget(self.stop_button)

        sidebar_layout.addStretch()

        self.result_label = QLabel("SYSTEM IDLE")
        self.result_label.setObjectName("ResultIndicator")
        sidebar_layout.addWidget(self.result_label)

        self.status_label = QLabel('Ready to start')
        self.status_label.setObjectName("StatusLabel")
        self.status_label.setWordWrap(True)
        sidebar_layout.addWidget(self.status_label)

        # --- Viewport ---
        viewport = QWidget()
        viewport_layout = QVBoxLayout(viewport)
        viewport_layout.setContentsMargins(20, 20, 20, 20)

        video_frame = QFrame()
        video_frame.setObjectName("VideoContainer")
        video_frame_layout = QVBoxLayout(video_frame)
        video_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("Camera feed will appear here")
        self.image_label.setStyleSheet("color: #444444; font-size: 18px;")
        video_frame_layout.addWidget(self.image_label)

        viewport_layout.addWidget(video_frame)

        # Assemble Main Layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(viewport, 1)

        # Populate camera sources
        self.populate_sources()

    def populate_sources(self):
        self.source_combo.clear()
        # Using CAP_DSHOW on Windows is much faster for device discovery
        for i in range(2): 
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                self.source_combo.addItem(f'Camera {i}', i)
                cap.release()
        if self.source_combo.count() == 0:
            self.source_combo.addItem('No camera found', -1)

    def start_detection(self):
        idx = self.source_combo.currentData()
        if idx == -1:
            self.status_label.setText('ERROR: No camera available!')
            return
        if self.capture is not None:
            self.capture.release()
        self.capture = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if not self.capture.isOpened():
            self.status_label.setText(f'ERROR: Failed to open Camera {idx}')
            return
        self.timer.start(30)
        self.status_label.setText('System Active: Detecting...')
        self.image_label.setText("") # Clear placeholder

    def stop_detection(self):
        self.timer.stop()
        if self.capture:
            self.capture.release()
            self.capture = None
        self.image_label.clear()
        self.image_label.setText("Camera feed will appear here")
        self.status_label.setText('System Standby')
        self.result_label.setText("SYSTEM IDLE")
        self.result_label.setStyleSheet("") # Reset to default QSS

    def update_frame(self):
        if self.capture is None or not self.capture.isOpened():
            return
        ret, frame = self.capture.read()
        if not ret:
            self.status_label.setText('ERROR: Lost camera feed')
            return
        # Run YOLOv8 segmentation
        results = self.model.predict(frame, device=self.device, verbose=False)
        annotated = results[0].plot()
        # Convert to QImage
        rgb_image = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        
        # Update result indicator
        has_crack = len(results[0].boxes) > 0
        if has_crack:
            self.result_label.setText("CRACK DETECTED")
            self.result_label.setStyleSheet("background-color: #FF2E63; color: white;")
        else:
            self.result_label.setText("NO CRACK")
            self.result_label.setStyleSheet("background-color: #2ECC71; color: white;")

        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def closeEvent(self, event):
        self.stop_detection()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model_path = 'runs/segment/runs/segment/biscuit_yolov8n_seg/weights/best.pt'
    window = CrackDetectorUI(model_path)
    window.show()
    sys.exit(app.exec_())
