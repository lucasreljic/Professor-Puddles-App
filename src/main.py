import cv2
import sys
import json
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QInputDialog, QComboBox, QStackedWidget
import pose_detector

#adjust file paths for pyinstaller
import sys
import os
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller one-file executable
        base_path = sys._MEIPASS
    else:
        # Running as a script
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

    # Now you can use json_file_path to read or write to your JSON file


class SettingsOverlay(QWidget):
    def __init__(self, back_action, loaded_data, user):
        super().__init__()

        self.back_action = back_action
        self.loaded_data = loaded_data
        self.user = user
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("Settings Page", self)
        font = QFont()
        font.setPointSize(16)  # Set font size to 16 (adjust as needed)
        font.setBold(True)     # Set font to bold
        self.title_label.setFont(font)  # Apply the font to the label
   
        self.layout.addWidget(self.title_label)  
        
        #comboBox
        self.texts_combo = QComboBox(self)
        self.layout.addWidget(self.texts_combo)
        self.texts_combo.setStyleSheet("QComboBox { background-color: #FFFFFF; color: black; width: 20px; padding: 10px 20px;  border-radius: 12px;}")
        self.texts_combo.setGeometry(10, 480, 100, 30)
        self.texts_combo.setFixedWidth(200)
        self.load_data_from_json()
        
        #Delete
        self.del_button = QPushButton("Delete User", self)
        self.del_button.setMaximumWidth(100)
        self.layout.addWidget(self.del_button)
        self.del_button.clicked.connect(self.delete_user)
        
        #enter 
        self.label_name = QLabel("Setup New User")
        self.layout.addWidget(self.label_name)
        self.button = QPushButton("Enter Name", self)
        self.layout.addWidget(self.button)  
        self.button.clicked.connect(self.show_name_input_dialog)

        self.name = ""

        
        #Close
        self.back_button = QPushButton("Close", self)
        self.back_button.setMaximumWidth(100)
        self.layout.addWidget(self.back_button)

        self.back_button.clicked.connect(self.back_to_main)

    def back_to_main(self):
        if self.back_action:
            self.user = self.texts_combo.currentIndex()
            self.back_action(self.user)
            
    def delete_user(self):
        if len(self.loaded_data) == 1:
            return
        index = self.texts_combo.currentText()
        self.loaded_data = [entry for entry in self.loaded_data if entry["name"] != str(index)]
        with open(resource_path('data.json'), 'w') as json_file:
            json.dump(self.loaded_data, json_file, indent=4, separators=(',', ':'))
        self.texts_combo.clear()  # Clear existing items
        for i in self.loaded_data:
                self.texts_combo.addItem(i["name"])  # Add items from the JSON data
        self.texts_combo.setCurrentIndex(0)
        
    def show_name_input_dialog(self):
        name, ok_pressed = QInputDialog.getText(self, "Enter Name", "Please enter your name:")
        if ok_pressed and name:
            self.name = name
            self.loaded_data.append({"name": name,
                                     "shoulder_nose_shoulder": 0,
                                            "left_shoulder": 0,
                                            "right_shoulder": 0 })
            with open(resource_path('data.json'), 'w') as json_file:
                json.dump(self.loaded_data, json_file, indent=4, separators=(',', ':'))
            self.texts_combo.clear()  # Clear existing items
            for i in self.loaded_data:
                self.texts_combo.addItem(i["name"])  # Add items from the JSON data
            self.texts_combo.setCurrentIndex(len(self.loaded_data)-1)
          
    def load_data_from_json(self):
        self.texts_combo.clear()  # Clear existing items
        for i in self.loaded_data:
            self.texts_combo.addItem(i["name"])  # Add items from the JSON data


        
class CameraViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        #setup detector
        self.detector = pose_detector.main()
        self.loaded_data = []
        self.i = 0
        #open json data file
        try:
            print("trying to access data")
            with open(resource_path('data.json')) as json_file:
                self.loaded_data = json.load(json_file)
        except FileNotFoundError:
            print("JSON file not found.")
        
        self.user = 0
            
        #pyqt stuff
        self.setWindowTitle("Professor Puddles")
        self.setFixedSize(600,600)
        self.menuWidget()
        self.setGeometry(600, 200, 600, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0,0,0,0)
        self.central_widget.setLayout(self.layout)
        
        
        #Settings button
        self.buttonSettings = QPushButton("", self)
        self.layout.addWidget(self.buttonSettings)
        self.buttonSettings.setMaximumSize(25,25)
        self.buttonSettings.setIcon(QIcon(resource_path("settings.png")))
        self.buttonSettings.clicked.connect(self.show_settings_page)
        
        #camera
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.layout.setAlignment(self.label, Qt.AlignCenter)
        pixmap = QPixmap('camera.png')
        pixmap.scaled(120, 100, 1)
        self.label.setPixmap(pixmap)
        
        #countdown stuff
        self.startCountdown = QPushButton("Collect Ideal Sitting Data", self)
        self.startCountdown.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 12px; }")
        self.startCountdown.setFont(QFont("Arial", 12, QFont.Bold))
        self.startCountdown.setGeometry(600,500, 100, 100)
        self.startCountdown.setMaximumWidth(800)
        self.collectData = False
        self.startCountdown.clicked.connect(self.isDataCollected)
        
        self.countTimer = QTimer()
        self.time_left = 10
        self.labelTimer = QLabel(self)
        self.countTimer.stop()
        self.labelTimer.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 12px; }")
        self.labelTimer.setFont(QFont("Arial", 12, QFont.Bold))
        self.labelTimer.setGeometry(300,400, 200, 100)
        self.labelTimer.setMaximumWidth(800)
        
        #start/stop button
        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 12px; }")
        self.start_stop_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.start_stop_button.setGeometry(600,600, 100, 100)
        self.start_stop_button.setMaximumWidth(200)
        self.layout.addWidget(self.start_stop_button)
        self.layout.setAlignment(self.start_stop_button, Qt.AlignCenter)
        self.start_stop_button.clicked.connect(self.toggle_camera)
        self.start_stop_button.move(QPoint(500,500))
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)
        self.optimizeTrig = False
        
        self.main_page = QWidget()
        self.stacked_widget.addWidget(self.main_page)

        self.settings_page = SettingsOverlay(self.back_to_main, self.loaded_data, self.user)
        self.stacked_widget.addWidget(self.settings_page)

        

        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera)
        self.capture = None
        self.camera_running = False
        
    def show_settings_page(self):
        self.buttonSettings.hide()
        self.label.hide()
        self.start_stop_button.hide()

        self.stacked_widget.setCurrentWidget(self.settings_page)

    def back_to_main(self, user):
        # Show main page widgets
        self.user = user
        self.buttonSettings.show()
        self.label.show()
        self.start_stop_button.show()
        self.stacked_widget.setCurrentWidget(self.main_page)

    def isDataCollected(self):
        self.collectData = True
        self.startCountdown.hide()
        
    def show_overlay(self):
        overlay_dialog = SettingsOverlay()
        overlay_dialog.setModal(True)
        overlay_dialog.exec_()
          
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
            self.labelTimer.clear()
            self.start_stop_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px 20px;  border-radius: 12px;}")
            self.start_stop_button.setText("Start")
        self.camera_running = not self.camera_running

    def update_camera(self):
        ret, frame = self.capture.read()
        frame = self.detector.find_pose(frame)
        # check if data exists
        if self.loaded_data[self.user]["shoulder_nose_shoulder"] == 0 or self.collectData:
            #data needs to be collected
            self.layout.addWidget(self.startCountdown)
            self.layout.setAlignment(self.startCountdown, Qt.AlignCenter)
            
        if(self.collectData):
            self.layout.addWidget(self.startCountdown)
            self.layout.setAlignment(self.startCountdown, Qt.AlignCenter)
            if not self.countTimer.isActive():
                self.countTimer.start()
                self.i = 0
            if self.time_left > 0:
                self.labelTimer.setText(str(round(self.time_left)) + "    ")
                self.time_left -= 1/10

            if self.time_left < 0:
                self.countTimer.stop() #stop the timer
                self.labelTimer.setText("Done!")
                self.loaded_data[self.user]["shoulder_nose_shoulder"] /= self.i # Average the data
                self.loaded_data[self.user]["left_shoulder"] /= self.i
                self.loaded_data[self.user]["right_shoulder"] /= self.i
                self.i = 0 # reset i counter
                with open(resource_path('data.json'), 'w') as json_file: # Save the data to the JSON file
                    json.dump(self.loaded_data, json_file, indent=4, separators=(',', ':'))
                self.collectData = False
            if ret:
                frame, data, _, self.i = pose_detector.run(frame, self.i, self.detector, self.loaded_data, self.user, True, entered_data=self.loaded_data)
                self.loaded_data = data
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (360, 300))    
                image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.label.setPixmap(pixmap)
        else:    
            if self.isMinimized() and not self.optimizeTrig: # update every 400ms if not visible
                self.timer.stop()
                self.timer.start(200)
                self.optimizeTrig = True
            elif not self.isMinimized() and self.optimizeTrig:# update every 10ms if visible
                self.timer.stop()
                self.timer.start(10)
                self.optimizeTrig = False
                
                
            if ret: # run the pose detector
                frame, data, _, self.i = pose_detector.run(frame, self.i, self.detector, self.loaded_data, self.user, False)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (360, 300))    
                image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.label.setPixmap(pixmap)
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CameraViewer()
    viewer.show()
    sys.exit(app.exec_())
