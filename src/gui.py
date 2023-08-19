import tkinter as tk
from tkinter.ttk import *
import cv2
import json
from main import main, run  
from PIL import Image, ImageTk
class GUI:
    def __init__(self, root, video_source=0, img = None):
        self.root = root
        self.root.title("Posture Corrector")#name
        self.root.geometry("800x400")# initial window size
        self.i  =0
        style = Style()
        style.theme_use("clam")# style of gui
        
        # Configure the style for the various widgets
        style.configure("TButton",
                        background="black",  # Background color
                        foreground="white",    # Text color
                        padding=10,            # Padding around the text
                        font=("Helvetica", 12, "bold"))

        style.configure("TLabel",
                        foreground="#333",    # Text color
                        font=("Helvetica", 14))

        style.configure("TEntry",
                        fieldbackground="white",  # Background color of the entry field
                        font=("Helvetica", 12))

        style.configure("TMenubutton",
                        background="white",   # Background color
                        font=("Helvetica", 12))
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        self.detector = main()
        width, height =  1080, 1920# Width of camera, #Height of Camera
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.label_widget = tk.Label(root)

        self.btn_start = Button(root, text="Start", width=10, command=self.start)
        self.btn_start.pack(padx=10, pady=5)

        self.btn_stop = Button(root, text="Stop", width=10, command=self.stop)
        self.btn_stop.pack(padx=10, pady=5)
        
        self.btn_start = Button(root, text="Setup" ,width=10, command=self.setup)
        self.btn_start.pack(padx=10, pady=5)
        # Read data from the JSON file
        self.firstRun = True
        self.integer = 0
        with open('data.json') as json_file:
            self.loaded_data = json.load(json_file)
        dropdown = [self.loaded_data[0]["name"],self.loaded_data[0]["name"], self.loaded_data[1]["name"], self.loaded_data[2]["name"], self.loaded_data[3]["name"]]
        
        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set(self.loaded_data[0]["name"])
        dropdown = OptionMenu(root, self.dropdown_var, *dropdown)
        print(self.dropdown_var.get())
        dropdown.pack()
        self.label_widget.pack()
        
        self.is_playing = False
        self.update()

    def start(self):
        if(not self.is_playing):
            self.is_playing = True
            self.firstRun = True
            self.update()

    def stop(self):
        self.is_playing = False

    def setup(self):
        self.firstRun = True
        entry1 = tk.Entry(self.root) 
        # canvas1.create_window(200, 140, window=entry1)
        # data
        # with open("data.json", "w") as json_file:
        #     json.dump(data, json_file, indent=4)
        self.setup = False
    def update(self):
        # Capture the video frame by frame
        if self.firstRun:
            for index, record in enumerate(self.loaded_data):
                if record["name"] == str(self.dropdown_var.get()):
                    self.integer = index
                    self.firstRun = False
        _, img = self.vid.read()
        img = run(img, self.i, self.detector, self.loaded_data, self.integer)
        opencv_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)


        # needs to be here cannot be in backend
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
    #app.update(img)

    root.mainloop()
    
if __name__ == "__main__":	
    gui()
    