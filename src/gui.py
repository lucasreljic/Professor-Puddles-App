import tkinter as tk
from tkinter import Canvas, OptionMenu
import cv2
import json
from main import main
from PIL import Image, ImageTk
from windows_toasts import Toast, WindowsToaster

# Set up toaster for notifs
toaster = WindowsToaster('Python')
newToast = Toast()


class GUI:

    def __init__(self, root, video_source=0):
        self.root = root
        self.root.title("Posture Corrector")
        self.root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        self.detector = main()
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 2020)

        self.label_widget = tk.Label(root, bg="white", borderwidth=2, relief="solid")
        self.label_widget.place(relx=0.6, rely=0.1, relwidth=0.3, relheight=0.7)

        self.btn_start = self.create_rounded_button("Start", "light green", self.start, 0.05, 0.1)
        self.btn_stop = self.create_rounded_button("Stop", "#FF8888", self.stop, 0.05, 0.3)
        self.btn_setup = self.create_rounded_button("Setup", "light blue", self.setup, 0.05, 0.5)

        dropdown_var = tk.StringVar()
        dropdown_var.set("Configs")

        with open('data.json') as json_file:
            loaded_data = json.load(json_file)["people"]
        dropdown = [loaded_data[i]["name"] for i in range(4)]

        dropdown_menu = OptionMenu(root, dropdown_var, *dropdown)
        dropdown_menu.place(relx=0.05, rely=0.7)

        self.is_playing = False
        self.update()

    def create_rounded_button(self, text, color, cmd, relx, rely):
        canvas = Canvas(self.root, bg='white', bd=0, highlightthickness=0, relief='ridge')
        canvas.place(relx=relx, rely=rely, relwidth=0.15, relheight=0.1)
        canvas.create_rectangle(10, 10, 10 + 150, 10 + 40, outline=color, fill=color, width=2)
        btn_id = canvas.create_text(85, 30, text=text, fill='white', font=("Helvetica", 12, "bold"))
        canvas.tag_bind(btn_id, '<ButtonPress-1>', lambda event, c=cmd: c())

        return canvas

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

        if not good_poster:
            newToast.text_fields = ['!']
            newToast.on_activated = lambda _: print('Toast clicked!')
            toaster.show_toast(newToast)
        # self.detector.showFps(frame)
        opencv_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

        if self.is_playing:
            opencv_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            captured_image = Image.fromarray(opencv_image)
            photo_image = ImageTk.PhotoImage(image=captured_image)
            self.label_widget.photo_image = photo_image
            self.label_widget.configure(image=photo_image)
            self.label_widget.after(10, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


def gui():
    root = tk.Tk()
    root.configure(bg="white")
    root.bind('<Escape>', lambda e: root.quit())
    app = GUI(root)

    root.mainloop()


if __name__ == "__main__":
    gui()
