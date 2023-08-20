import cv2
import mediapipe as mp
import math

from windows_toasts import Toast, WindowsToaster

toaster = WindowsToaster('Python')
newToast = Toast()


class FrontPoseDetector():
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
        # some time this angle comes zero, so below conditon we added
        if angle < 0:
            angle += 360

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 1)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 1)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 1)
            # cv2.putText(img, str(int(angle)), (x2 - 20, y2 + 50), cv2.FONT_HERSHEY_SIMPLEX,
            #             1, (0, 0, 255), 2)
        return angle


def run(img, i, detector, data, dropdown):
    i += 1

    # Setup
    img = detector.find_pose(img)
    detector.get_position(img)  # DO NOT DELETE: this will give the landmark list

    # Interested angle
    front_posture = detector.find_angle(img, 11, 0, 12)
    left_shoulder = detector.find_angle(img, 9, 11, 12)
    right_shoulder = detector.find_angle(img, 10, 12, 11)

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
    detector = FrontPoseDetector()
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
