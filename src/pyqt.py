import cv2
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
import pose_detector

class CameraViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.detector = pose_detector.main()
        self.setWindowTitle("OpenCV Camera Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        self.start_stop_button = QPushButton("Start Camera")
        self.start_stop_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 12px; }")
        self.start_stop_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.start_stop_button)

        self.start_stop_button.clicked.connect(self.toggle_camera)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera)

        self.capture = None
        self.camera_running = False
    def toggle_camera(self):
        if not self.camera_running:
            self.capture = cv2.VideoCapture(0)
            self.timer.start(10)  # Update every 10 milliseconds (adjust as needed)
            self.start_stop_button.setText("Stop Camera")
            self.start_stop_button.setStyleSheet("QPushButton { background-color: #F44336; color: white; padding: 10px 20px;  border-radius: 12px;}")
        else:
            if self.capture is not None:
                self.capture.release()
                self.timer.stop()
            self.start_stop_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px 20px;  border-radius: 12px;}")
            self.start_stop_button.setText("Start Camera")
        self.camera_running = not self.camera_running

    def update_camera(self):
        ret, frame = self.capture.read()
        frame = self.detector.find_pose(frame)
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CameraViewer()
    viewer.show()
    sys.exit(app.exec_())
