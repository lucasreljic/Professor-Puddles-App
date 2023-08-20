import cv2
import mediapipe as mp
import math

from windows_toasts import Toast, WindowsToaster

toaster = WindowsToaster('Python')
newToast = Toast()


class SidePoseDetector():

    def __init__(self, mode=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.pTime = 0

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode, smooth_landmarks=self.smooth,
                                     min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)

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


def run(img, i, detector, data, dropdown, getData, entered_data = None):
    i += 1

    # Setup
    img = detector.find_pose(img)
    detector.get_position(img)  # DO NOT DELETE: this will give the landmark list

    # Get the landmarks
    lmList = detector.get_position(img)

    x0, y0 = lmList[0][1], lmList[0][2]

    x2, y2 = lmList[2][1], lmList[2][2]
    x5, y5 = lmList[5][1], lmList[5][2]

    x7, y7 = lmList[7][1], lmList[7][2]
    x8, y8 = lmList[8][1], lmList[8][2]

    x11, y11 = lmList[11][1], lmList[11][2]
    x12, y12 = lmList[12][1], lmList[12][2]

    good_poster = True
    if getData:
        data[dropdown]["x0"] += x0  
        data[dropdown]["x2"] += x2
        data[dropdown]["x5"] += x5 
        data[dropdown]["x7"] += x7 
        data[dropdown]["x8"] += x8 
        data[dropdown]["x11"] += x11 
        data[dropdown]["x12"] += x12
        data[dropdown]["y0"] += y0 
        data[dropdown]["y2"] += y2 
        data[dropdown]["y5"] += y5 
        data[dropdown]["y7"] += y7 
        data[dropdown]["y8"] += y8 
        data[dropdown]["y11"] += y11 
        data[dropdown]["y12"] += y12 
        
        
    else:
        # The actual criteria for a good posture
        if x0 < data[dropdown]["x0"] - 200 or x0 > data[dropdown]["x0"] + 200 \
                or x2 < data[dropdown]["x2"] - 200 or x2 > data[dropdown]["x2"] + 200 \
                or x5 < data[dropdown]["x5"] - 200 or x5 > data[dropdown]["x5"] + 200 \
                or x7 < data[dropdown]["x7"] - 200 or x7 > data[dropdown]["x7"] + 200 \
                or x8 < data[dropdown]["x8"] - 200 or x8 > data[dropdown]["x8"] + 200 \
                or x11 < data[dropdown]["x11"] - 200 or x11 > data[dropdown]["x11"] + 200 \
                or x12 < data[dropdown]["x12"] - 200 or x12 > data[dropdown]["x12"] + 200 \
                or y0 > data[dropdown]["y0"] + 100 \
                or y2 > data[dropdown]["y2"] + 100 \
                or y5 > data[dropdown]["y5"] + 100 \
                or y7 > data[dropdown]["y7"] + 100 \
                or y8 > data[dropdown]["y8"] + 100 \
                or y11 > data[dropdown]["y11"] + 100 \
                or y12 > data[dropdown]["y12"] + 100:
            good_poster = False
        print(good_poster)

        # Send notifications if bad posture
        if not good_poster and i > 100:
            newToast.text_fields = ['Sit up straight!']
            newToast.on_activated = lambda _: print('Toast clicked!')
            toaster.show_toast(newToast)
            i = 0
    return img, entered_data


def main():
    detector = SidePoseDetector()
    # cap = cv2.VideoCapture(0)
    # while True:
    #     success, img = cap.read()
    #     img = detector.findPose(img)
    #     lmList = detector.getPosition(img)
    #     #print(lmList)
    #     print(detector.findAngle(img, 10, 11, 12))
    #     # detector.showFps(img)
    return detector


if __name__ == "__main__":
    main()
