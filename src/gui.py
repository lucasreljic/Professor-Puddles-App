import tkinter as tk
from tkinter.ttk import *
import cv2
import json
from main import main
from PIL import Image, ImageTk
from windows_toasts import Toast, WindowsToaster

# Set up toaster for notifs
toaster = WindowsToaster('Python')
newToast = Toast()


class GUI:

    def __init__(self, root, video_source=0, img=None):
        self.root = root
        self.root.title("Posture Corrector")
        self.root.geometry("800x400")
        self.i = 0
        style = Style()
        style.theme_use("clam")

        # Configure the style for the various widgets
        style.configure("TButton",
                        background="black",
                        foreground="white",
                        padding=10,
                        font=("Helvetica", 12, "bold"))

        style.configure("TLabel",
                        foreground="#333",
                        font=("Helvetica", 14))

        style.configure("TEntry",
                        fieldbackground="white",
                        font=("Helvetica", 12))

        style.configure("TMenubutton",
                        background="white",
                        font=("Helvetica", 12))
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        self.detector = main()
        width, height = 1080, 1920
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.label_widget = tk.Label(root)

        self.btn_start = Button(root, text="Start", width=10, command=self.start)
        self.btn_start.pack(padx=10, pady=5)

        self.btn_stop = Button(root, text="Stop", width=10, command=self.stop)
        self.btn_stop.pack(padx=10, pady=5)

        self.btn_start = Button(root, text="Setup", width=10, command=self.setup)
        self.btn_start.pack(padx=10, pady=5)
        dropdown_var = tk.StringVar()
        dropdown_var.set("Configs")

        # Read data from the JSON file
        with open('data.json') as json_file:
            loaded_data = json.load(json_file)["people"]
        dropdown = [loaded_data[0]["name"], loaded_data[1]["name"], loaded_data[2]["name"], loaded_data[3]["name"]]

        dropdown = OptionMenu(root, dropdown_var, *dropdown)
        dropdown.pack()
        self.label_widget.pack()

        self.is_playing = False
        self.update()

    def start(self):
        if (not self.is_playing):
            self.is_playing = True
            self.update()

    def stop(self):
        self.is_playing = False

    def setup(self):
        entry1 = tk.Entry(self.root)
        # canvas1.create_window(200, 140, window=entry1)
        # data
        # with open("data.json", "w") as json_file:
        #     json.dump(data, json_file, indent=4)
        self.setup = False

    def update(self):
        # Capture the video frame by frame

        _, img = self.vid.read()
        self.i += 1

        # Setup
        img = self.detector.find_pose(img)
        self.detector.get_position(img)  # DO NOT DELETE: this will give the landmark list

        # Interested angle
        # r_turn = self.detector.find_angle(img, 6, 8, 0)
        # l_turn = self.detector.find_angle(img, 3, 7, 0)
        front_posture = self.detector.find_angle(img, 11, 0, 12)
        left_shoulder = self.detector.find_angle(img, 9, 11, 12)
        right_shoulder = self.detector.find_angle(img, 10, 12, 11)

        good_poster = True

        # TODO: add an interator for good_posture so it only sends a notification if you slouch
        #  for a certain amount of time

        # TODO: right now the following measurements are for me. we need code to make it personalized
        if front_posture < 75 \
                or front_posture > 95 \
                or left_shoulder < 310 or left_shoulder > 320 \
                or right_shoulder < 40 or right_shoulder > 50:
            good_poster = False
        print(good_poster)

        if not good_poster and self.i > 100:
            newToast.text_fields = ['!']
            newToast.on_activated = lambda _: print('Toast clicked!')
            toaster.show_toast(newToast)
            self.i = 0
        # self.detector.showFps(frame)
        opencv_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

        if self.is_playing:
            # Convert image from one color space to other
            opencv_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

            # Capture the latest img and transform to image
            captured_image = Image.fromarray(opencv_image)

            # Convert captured image to photoimage
            photo_image = ImageTk.PhotoImage(image=captured_image)

            # Displaying photoimage in the label
            self.label_widget.photo_image = photo_image

            # Configure image in the label
            self.label_widget.configure(image=photo_image)

            # Repeat the same process after every 10 seconds
            self.label_widget.after(10, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


def gui():
    root = tk.Tk()
    root.bind('<Escape>', lambda e: app.quit())
    app = GUI(root)
    # app.update(img)

    root.mainloop()


if __name__ == "__main__":
    gui()
