import cv2
import sys
import json
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QInputDialog, QComboBox
import pose_detector


class CameraViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        #setup detector
        self.detector = pose_detector.main()
        self.i = 0
        #open json data file
        try:
            with open('data.json') as json_file:
                self.loaded_data = json.load(json_file)
        except FileNotFoundError:
            print("JSON file not found.")
            
            
        #pyqt stuff
        self.setWindowTitle("Professor Puddles")
        self.setFixedSize(600,600)
        self.menuWidget()
        self.setGeometry(100, 100, 600, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        
        #enter name
        self.button = QPushButton("Enter Name", self)
        self.button.setGeometry(10, 480, 100, 30)
        self.button.clicked.connect(self.show_name_input_dialog)

        self.name = ""

        #comboBox
        self.texts_combo = QComboBox(self)
        self.layout.addWidget(self.texts_combo)
        self.texts_combo.setStyleSheet("QComboBox { background-color: #FFFFFF; color: black; width: 20px; padding: 10px 20px;  border-radius: 12px;}")
        self.texts_combo.setGeometry(10, 480, 100, 30)
        self.load_data_from_json()
        
        #start/stop button
        self.start_stop_button = QPushButton("Start Camera")
        self.start_stop_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 12px; }")
        self.start_stop_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.start_stop_button.setGeometry(150, 100, 800, 300)
        self.layout.addWidget(self.start_stop_button)
        
        self.start_stop_button.clicked.connect(self.toggle_camera)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera)

        self.capture = None
        self.camera_running = False
        
        
    def show_name_input_dialog(self):
        name, ok_pressed = QInputDialog.getText(self, "Enter Name", "Please enter your name:")
        if ok_pressed and name:
            self.name = name
            print(f"Entered Name: {self.name}")
            self.loaded_data.append({"name": name,
                                     "shoulder_nose_shoulder": 0,
                                            "left_shoulder": 0,
                                            "right_shoulder": 0 })
            with open('data.json', 'w') as json_file:
                json.dump(self.loaded_data, json_file, indent=4, separators=(',', ':'))
            self.texts_combo.clear()  # Clear existing items
            for i in self.loaded_data:
                self.texts_combo.addItem(i["name"])  # Add items from the JSON data
            

          
    def load_data_from_json(self):
        self.texts_combo.clear()  # Clear existing items
        for i in self.loaded_data:
            self.texts_combo.addItem(i["name"])  # Add items from the JSON data


  
    def toggle_camera(self):
        if not self.camera_running:
            self.capture = cv2.VideoCapture(0)
            self.timer.start(10)  # Update every 10 milliseconds (adjust as needed)
            self.start_stop_button.setText("Stop")
            self.start_stop_button.setStyleSheet("QPushButton { background-color: #F44336; color: white; padding: 10px 20px;  border-radius: 12px;}")
        else:
            if self.capture is not None:
                self.capture.release()
                self.timer.stop()
            self.start_stop_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px 20px;  border-radius: 12px;}")
            self.start_stop_button.setText("Start")
        self.camera_running = not self.camera_running

    def update_camera(self):
        ret, frame = self.capture.read()
        frame = self.detector.find_pose(frame)
        if ret:
            frame, data, _, self.i = pose_detector.run(frame, self.i, self.detector, self.loaded_data, 0, False)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.label.setPixmap(pixmap)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CameraViewer()
    viewer.show()
    sys.exit(app.exec_())
