import cv2
import mediapipe as mp
import math
import pygame
import time
from windows_toasts import Toast, WindowsToaster
import threading

toaster = WindowsToaster('Python')
newToast = Toast()


class PoseDetector():
    def __init__(self, mode=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.pTime = 0
        pygame.init()
        pygame.mixer.init()
        self.quack = pygame.mixer.Sound("Quack.wav")
        self.stopSlouch = pygame.mixer.Sound("Stop.wav")
        self.finalSlouch = pygame.mixer.Sound("Final.wav")
        
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode, smooth_landmarks=self.smooth,
                                     min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)
        print(self.detectionCon)

    def find_pose(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def get_position(self, img):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
        return self.lmList

    def find_angle(self, img, p1, p2, p3, draw=True):
        # Get the landmark
        try:
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]
            x3, y3 = self.lmList[p3][1:]
        except:
            x1 = 0
            y1 = 0
            x2 = 0
            y2 = 0
            x3 = 0
            y3 = 0
            print("out of bounds")

        # Calculate the angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        # some time this angle comes zero, so below condition we added
        if angle < 0:
            angle += 360

        # # Draw comment out for faster performance
        # if draw:
        #     cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
        #     cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
        #     cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (x1, y1), 15, (0, 0, 255), 1)
        #     cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (x2, y2), 15, (0, 0, 255), 1)
        #     cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (x3, y3), 15, (0, 0, 255), 1)
        #     # cv2.putText(img, str(int(angle)), (x2 - 20, y2 + 50), cv2.FONT_HERSHEY_SIMPLEX,
        #     #             1, (0, 0, 255), 2)
        return angle
        
    def run(self, img, i, data, dropdown, getData, entered_data = None, timer = 0):
        i += 1

        # Setup
        img = self.find_pose(img)
        self.get_position(img)  # DO NOT DELETE: this will give the landmark list

        # Interested angle
        front_posture = self.find_angle(img, 11, 0, 12)
        left_shoulder = self.find_angle(img, 9, 11, 12)
        right_shoulder = self.find_angle(img, 10, 12, 11)

        good_poster = True
        if getData:
            entered_data[dropdown]["shoulder_nose_shoulder"] += front_posture
            entered_data[dropdown]["left_shoulder"] += left_shoulder
            entered_data[dropdown]["right_shoulder"] += right_shoulder
        else:    
            # The actual criteria for a good posture
            if front_posture < data[dropdown]["shoulder_nose_shoulder"] - 10 \
                    or front_posture > data[dropdown]["shoulder_nose_shoulder"] + 10 \
                    or left_shoulder < data[dropdown]["left_shoulder"] - 10 \
                    or left_shoulder > data[dropdown]["left_shoulder"] + 10 \
                    or right_shoulder < data[dropdown]["right_shoulder"] - 10 \
                    or right_shoulder > data[dropdown]["right_shoulder"] + 10:

                good_poster = False

            if good_poster and 4 < (time.time() - timer) < 11:
                if i > 0:
                    i -=2
                timer = time.time()
                print("countdown terminated")
            elif good_poster:
                if i > 0:
                        i -=2
                timer = time.time()
            #print(good_poster)
            #print(i)
            # Send notifications if bad posture
            if not good_poster and i < 52 and i > 50:
                print("first warning")
                newToast.text_fields = ['Sit up straight!']
                toaster.show_toast(newToast)
                self.quack.play()
            if  not good_poster and i < 152 and i > 150:
                print("second warning")
                for j in range(3): #quack 3 times
                    self.quack.play()
                    time.sleep(0.5)
                newToast.text_fields = ['Sit up straight I mean it!']
                toaster.show_toast(newToast)
            elif not good_poster and i < 200 and i > 198:
                timer = time.time()
                print("third warning")
                newToast.text_fields = ["Sit up or I delete system32!"]
                toaster.show_toast(newToast)
                self.stopSlouch.play()
            elif not good_poster and i > 400 and time.time() - timer > 11:
                #kill computer
                print("countdown completed")
                self.finalSlouch.play()
                newToast.text_fields = ["Deleting system32..."]
                toaster.show_toast(newToast)
                time.sleep(0.01)
                i = 0
                
                
        return img, entered_data, timer, i
