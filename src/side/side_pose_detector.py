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

def run(img, i, detector, data, dropdown):
    i += 1

    # Setup
    img = detector.find_pose(img)
    detector.get_position(img)  # DO NOT DELETE: this will give the landmark list

    # Get the landmarks


    good_poster = True

    # The actual criteria for a good posture
    if front_posture < data[dropdown]["shoulder_nose_shoulder"] - 10 \
            or front_posture > data[dropdown]["shoulder_nose_shoulder"] + 10 \
            or left_shoulder < data[dropdown]["left_shoulder"] - 10 \
            or left_shoulder > data[dropdown]["left_shoulder"] + 10 \
            or right_shoulder < data[dropdown]["right_shoulder"] - 10 \
            or right_shoulder > data[dropdown]["right_shoulder"] + 10:

        good_poster = False

    print(good_poster)

    # Send notifications if bad posture
    if not good_poster and i > 100:
        newToast.text_fields = ['Sit up straight!']
        newToast.on_activated = lambda _: print('Toast clicked!')
        toaster.show_toast(newToast)
        i = 0
    return img


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
