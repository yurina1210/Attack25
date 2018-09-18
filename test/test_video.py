import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from time import sleep
import numpy as np

# 表示サイズ
PANEL_SIZE = 140
PANEL_NUM = 5
MARGIN = 20
MARGIN_LEFT = 10
CANVAS_SIZE = PANEL_SIZE * PANEL_NUM + MARGIN*2# + MARGIN_LEFT*2
TEXT_FONT = ('Calibre', PANEL_SIZE//2)
colors = [
    "#c6001c", # 1-red
    "#228b22", # 2-forestgreen
    "#ffffff", # 3-white
    "#1C6ECD", # 4-blue
    "#800080", # 5-purple
    "#ffa500", # 6-orange
    "#00ff7f", # 7-springgreen
    "#00ffff", # 8-cyan
    "#f5deb3", # 9-wheat
    "#ffc0cb" # 10-pink
]
window_w, window_h = 0, 0
panel_w, panel_h = 0, 0

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.attributes('-fullscreen', True)
        self.window.bind("<Escape>", lambda e: e.widget.quit())
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = window_w, height = window_h)
        self.canvas.pack()
        self.panels = []
        ret, frame = self.vid.get_frame()
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.delay = int(1000.0 / self.vid.fps)
        print(self.delay, "ms")

        # パネルの情報を読み込み
        for i in range(4):
            path = "datas/champ_panels" + str(i) + ".txt"
            self.data = open(path, "r")
            self.panels.append(self.data.readlines())

        num_panels = [self.panels[i].__len__() for i in range(4)]
        np_array = np.array(num_panels)
        self.max_i = np.argmax(np_array)

        for k in reversed(range(self.panels[self.max_i].__len__())):
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            for i in range(k):
                n = int(self.panels[self.max_i][i])
                x = panel_w * (n%PANEL_NUM)
                y = panel_h * (n//PANEL_NUM)
                self.canvas.create_rectangle(x, y, x+panel_w, y+panel_h, fill=colors[self.max_i], tag='free')
                self.canvas.create_text(x+(panel_w/2),y+(panel_h/2),text=str(n+1),font=TEXT_FONT, tag='label')
                
            for i in range(4):
                if i != self.max_i:
                    for n_str in self.panels[i]:
                        n = int(n_str)
                        x = panel_w * (n%PANEL_NUM)
                        y = panel_h * (n//PANEL_NUM)
                        self.canvas.create_rectangle(x, y, x+panel_w, y+panel_h, fill=colors[i], tag='free')
                        self.canvas.create_text(x+(panel_w/2),y+(panel_h/2),text=str(n+1),font=TEXT_FONT, tag='label')
            
            sleep(0.5)
            self.window.update()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.update()

        self.window.mainloop()

    
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        
        for i in range(4):
            if i != self.max_i:
                for n_str in self.panels[i]:
                    n = int(n_str)
                    x = panel_w * (n%PANEL_NUM)
                    y = panel_h * (n//PANEL_NUM)
                    self.canvas.create_rectangle(x, y, x+panel_w, y+panel_h, fill=colors[i], tag='free')
                    self.canvas.create_text(x+(panel_w/2),y+(panel_h/2),text=str(n+1),font=TEXT_FONT, tag='label')
        
        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)

    def get_frame(self):
        if self.vid.isOpened():
            ret, _frame = self.vid.read()
            size = (window_w, window_h)
            frame = cv2.resize(_frame, size, interpolation = cv2.INTER_CUBIC)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                 return (ret, None)
        else:
            return (ret, None)
 
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
 
# Create a window and pass it to the Application object
root = tkinter.Tk()
window_w, window_h = root.winfo_screenwidth(), root.winfo_screenheight()
panel_w = int(window_w / PANEL_NUM)
panel_h = int(window_h / PANEL_NUM)
App(root, "Tkinter and OpenCV", "movies/breakdance.mp4")