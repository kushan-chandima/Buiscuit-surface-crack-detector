import sys
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from ultralytics import YOLO
import torch

class CrackDetectorUI(QMainWindow):
	def __init__(self, model_path):
		super().__init__()
		self.setWindowTitle('Biscuit Crack Detector')
		self.model = YOLO(model_path)
		self.capture = None
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_frame)
		self.device = 'cpu'  # Force CPU usage

		# UI Elements
		self.image_label = QLabel()
		self.image_label.setAlignment(Qt.AlignCenter)
		self.start_button = QPushButton('Start')
		self.stop_button = QPushButton('Stop')
		self.source_combo = QComboBox()
		self.status_label = QLabel('Select camera and press Start')

		self.start_button.clicked.connect(self.start_detection)
		self.stop_button.clicked.connect(self.stop_detection)

		# Populate camera sources
		self.populate_sources()

		# Layout
		btn_layout = QHBoxLayout()
		btn_layout.addWidget(self.source_combo)
		btn_layout.addWidget(self.start_button)
		btn_layout.addWidget(self.stop_button)

		layout = QVBoxLayout()
		layout.addLayout(btn_layout)
		layout.addWidget(self.image_label)
		layout.addWidget(self.status_label)

		container = QWidget()
		container.setLayout(layout)
		self.setCentralWidget(container)

	def populate_sources(self):
		# Try first 5 camera indices
		self.source_combo.clear()
		for i in range(5):
			cap = cv2.VideoCapture(i)
			if cap.isOpened():
				self.source_combo.addItem(f'Camera {i}', i)
				cap.release()
		if self.source_combo.count() == 0:
			self.source_combo.addItem('No camera found', -1)

	def start_detection(self):
		idx = self.source_combo.currentData()
		if idx == -1:
			self.status_label.setText('No camera available!')
			return
		self.capture = cv2.VideoCapture(idx)
		self.timer.start(30)
		self.status_label.setText('Detecting...')

	def stop_detection(self):
		self.timer.stop()
		if self.capture:
			self.capture.release()
		self.image_label.clear()
		self.status_label.setText('Detection stopped.')

	def update_frame(self):
		if self.capture is None or not self.capture.isOpened():
			return
		ret, frame = self.capture.read()
		if not ret:
			return
		# Run YOLOv8 segmentation
		results = self.model.predict(frame, device=self.device, verbose=False)
		annotated = results[0].plot()
		# Convert to QImage
		rgb_image = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
		h, w, ch = rgb_image.shape
		bytes_per_line = ch * w
		qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
		self.image_label.setPixmap(QPixmap.fromImage(qt_image))

	def closeEvent(self, event):
		self.stop_detection()
		event.accept()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	model_path = 'runs/segment/biscuit_yolov8n_seg/weights/best.pt'  # Update if needed
	window = CrackDetectorUI(model_path)
	window.resize(900, 700)
	window.show()
	sys.exit(app.exec_())
