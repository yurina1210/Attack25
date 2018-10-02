import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from PIL import Image
import time
from time import sleep
import numpy as np
import threading
import os
from pathlib import Path
import pygame

# 表示サイズ
PANEL_SIZE = 140
PANEL_NUM = 5
MARGIN = 20
MARGIN_LEFT = 10
CANVAS_SIZE = PANEL_SIZE * PANEL_NUM + MARGIN*2# + MARGIN_LEFT*2
TEXT_FONT = ('Calibre', PANEL_SIZE//2, ' bold')
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
color_names = [
    "赤","緑","白","青"
]
window_w, window_h = 0, 0
panel_w, panel_h = 0, 0

# 音声ファイルの読み込み
pygame.mixer.pre_init(frequency=48000, size = -16, channels = 2, buffer = 1024*4)
pygame.mixer.init()
sound = pygame.mixer.Sound('../sounds/film_quiz.wav')
length_seconds = sound.get_length()
print(length_seconds , "s")

# 画像ファイルの読み込み
p = Path("../photo_for_film_quiz/")
img_paths = list(p.glob("*.jpg"))
img_paths.sort()
num_of_frames = int(img_paths.__len__())

'''
# パネルの情報を読み込み
panels = []
for i in range(4):
    path = "datas/champ_panels" + str(i) + ".txt"
    data = open(path, "r")
    panels.append(data.readlines())

num_panels = [panels[i].__len__() for i in range(4)]
np_array = np.array(num_panels)
max_i = [i for i, x in enumerate(np_array) if x == max(np_array)]
if max_i.__len__() == 1:
    num = panels[max_i].__len__()
else:
    for i in max_i:
        print(color_names[i], ",") 
    print("が同率首位です．どちらが優勝者か入力してください．")
    print("赤 => 0\n緑 => 1\n白 => 2\n青 => 3")
    max_i = input('>>>  ')
    print("max_i: ",max_i)
'''

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.overrideredirect(True)
        self.window.attributes('-fullscreen', True)
        self.window.attributes('-topmost', True)
        self.window.overrideredirect(False)
        self.window.bind("<Escape>", lambda e: e.widget.quit())
        self.window.title(window_title)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = window_w, height = window_h)
        self.canvas.pack()
        self.panels = []
        self.seq = 0
        
        im = Image.open(img_paths[self.seq])
        self.photo = PIL.ImageTk.PhotoImage(image = im.resize((window_w, window_h)))
    
        self.delay = int(length_seconds / num_of_frames * 1000)
        print(self.delay, "s")

        # パネルの情報を読み込み
        for i in range(4):
            path = "../datas/champ_panels" + str(i) + ".txt"
            self.data = open(path, "r")
            self.panels.append(self.data.readlines())

        num_panels = [self.panels[i].__len__() for i in range(4)]
        np_array = np.array(num_panels)
        max_index = [i for i, x in enumerate(np_array) if x == max(np_array)]
        if max_index.__len__() == 1:
            self.max_i = max_index[0]
            num = self.panels[self.max_i].__len__()
        else:
            for i in max_index:
                print(color_names[i], ",") 
            print("が同率首位です．どちらが優勝者か入力してください．")
            print("赤 => 0\n緑 => 1\n白 => 2\n青 => 3")
            self.max_i = int(input(''))

        for k in reversed(range(self.panels[self.max_i].__len__())):
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            for i in range(k):
                n = int(self.panels[self.max_i][i])
                x = panel_w * (n%PANEL_NUM)
                y = panel_h * (n//PANEL_NUM)
                self.canvas.create_rectangle(x, y, x+panel_w, y+panel_h, fill=colors[self.max_i], tag='free', width=4)
                self.canvas.create_text(x+(panel_w/2),y+(panel_h/2),text=str(n+1),font=TEXT_FONT, tag='label')
                
            for i in range(4):
                if i != self.max_i:
                    for n_str in self.panels[i]:
                        n = int(n_str)
                        x = panel_w * (n%PANEL_NUM)
                        y = panel_h * (n//PANEL_NUM)
                        self.canvas.create_rectangle(x, y, x+panel_w, y+panel_h, fill=colors[i], tag='free', width=4)
                        self.canvas.create_text(x+(panel_w/2),y+(panel_h/2),text=str(n+1),font=TEXT_FONT, tag='label')
            
            sleep(0.5)
            self.window.update()

        th = threading.Thread(name="a", target=sound.play)
        th.start()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.update()

        self.window.mainloop()

    
    def update(self):
        im = Image.open(img_paths[self.seq])
        im_resize = im.resize((window_w, window_h))
        self.photo = PIL.ImageTk.PhotoImage(image = im_resize)
        self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        
        for i in range(4):
            if i != self.max_i:
                for n_str in self.panels[i]:
                    n = int(n_str)
                    x = panel_w * (n%PANEL_NUM)
                    y = panel_h * (n//PANEL_NUM)
                    self.canvas.create_rectangle(x, y, x+panel_w, y+panel_h, fill=colors[i], tag='free', width=4)
                    self.canvas.create_text(x+(panel_w/2),y+(panel_h/2),text=str(n+1),font=TEXT_FONT, tag='label')
        
        # Get a frame from the video source
        if self.seq < num_of_frames-1:
            self.seq += 1

        print("seq: ", self.seq, "num: ", num_of_frames)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self):
        # Get video source width and height
        im = Image.open(img_paths[self.seq])
        im_resize = im.resize((window_w, window_h))
        self.photo = PIL.ImageTk.PhotoImage(image = im_resize)
        self.height, self.width, self.channels = im_resize.shape
 
# Create a window and pass it to the Application object
root = tkinter.Tk()
window_w, window_h = root.winfo_screenwidth(), root.winfo_screenheight()
panel_w = int(window_w / PANEL_NUM)
panel_h = int(window_h / PANEL_NUM)

App(root, "最終問題")