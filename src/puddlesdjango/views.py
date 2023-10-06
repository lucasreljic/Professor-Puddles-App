# views.py
import cv2
from django.http import StreamingHttpResponse
from django.views import View
import pose_detector

class CameraView(View):
    def get(self, request):
        # Open the camera
        cap = cv2.VideoCapture(0)  # 0 for default camera (you can specify a different camera index if needed)

        def generate_frames():
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                detector = pose_detector.main()
                frame = detector.find_pose(frame)
                #lmList = detector.get_position(frame)
                # Convert the frame to JPEG format
                _, buffer = cv2.imencode('.jpg', frame)
                frame_data = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

        return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')