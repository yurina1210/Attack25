import socket
import cv2
import numpy as np
import tkinter as tk
import threading
import pygame
from PIL import Image, ImageTk

# チームごとのデータ(色，IPアドレス，音声データ，etc...)
colors = [
    "#FF001c", # 1-red
    "#228b22", # 2-forestgreen
    "#FFFFFF", # 3-white
    "#1C6ECD", # 4-blue
    "#800080", # 5-purple
    "#ffa500", # 6-orange
    "#00ff7f", # 7-springgreen
    "#00ffff", # 8-cyan
    "#f5deb3", # 9-wheat
    "#ffc0cb" # 10-pink
]

ip_adress = [
    '192.168.0.3', #赤
    '192.168.0.4', #緑
    '192.168.0.5', #白
    '192.168.0.6'  #青
]
'''
# チームごとに早押しBGMを変える場合
bgm_paths = [
    '../bgms/0.mp3',
    '../bgms/1.mp3',
    '../bgms/2.mp3',
    '../bgms/3.mp3'
]
'''

# IPアドレスからチームカラーを決定
ip = socket.gethostbyname(socket.gethostname())
team_id = 0
for i in range(4):
    if ip == ip_adress[i]:
        team_id = i
        break

team_color = colors[team_id]
#team_bgm = bgm_paths[team_id]
team_bgm = "../sounds/hayaoshi.wav"
team_ip = ip_adress[team_id]



# 変数
edge_wide = 40

# pygame初期化
pygame.mixer.pre_init(48000,-16,2,1024)
pygame.mixer.init()
pygame.mixer.music.load(team_bgm)

flag = False
judge = 1
score = str(0)

root = tk.Tk()
window_w, window_h = root.winfo_screenwidth(), root.winfo_screenheight()
TEXT_FONT = ('Calibre', window_w//2, ' bold')
root.canvas = tk.Canvas(root, width = window_w, height = window_h, bg=team_color, highlightthickness=0)
root.canvas.create_rectangle(edge_wide, edge_wide ,window_w-edge_wide, window_h-edge_wide, fill='black')
root.canvas.create_text(int(window_w * 0.5), int(window_h * 0.5), text=int(score), font=TEXT_FONT, fill='white')
root.canvas.pack()

# 早押し(Fastest Finger First)管理関数
def fff(event):
    global flag
    global judge

    '''
    # 早押し機能使わない場合以下をコメントアウト
    #サーバとの通信
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # サーバを指定
        s.bind((team_ip,50007))
        # サーバにメッセージを送る
        #num = str(count)
        color_id = str(0)
        s.sendall(color_id.encode('utf-8'))
        # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
        data = s.recv(1024)
        judge = int(data)
        print(judge)
    '''

    if not flag and judge == 1:
        flag = True

        root.canvas.delete('all')
        root.canvas.create_rectangle(0, 0 ,window_w, window_h, fill=team_color)
        if team_id == 2:
            fill = 'black'
        else:
            fill = 'white'
        root.canvas.create_text(int(window_w * 0.5), int(window_h * 0.5), text=int(score), font=TEXT_FONT, fill=fill)
    
    pygame.mixer.music.play(1)
    


root.overrideredirect(True)
#root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.overrideredirect(False)
root.bind("<Return>", fff)

def print_num():
    global score
    global flag
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        #4台のPCと実際に通信するとき
        s.bind((team_ip, 50007))

        #ローカルでテストする場合
        #s.bind(('127.0.0.1',50007))

        #テスト用
        #s.bind(('192.168.0.8', 50007))
        s.listen(1)

        while True:    
            conn,addr = s.accept()
            with conn:

                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    score = data.decode('utf-8')
                    root.canvas.delete('all')
                    root.canvas.delete('all')
                    root.canvas.create_rectangle(0, 0 , window_w, window_h, fill=team_color)
                    root.canvas.create_rectangle(edge_wide, edge_wide ,window_w-edge_wide, window_h-edge_wide, fill='black')
                    root.canvas.create_text(int(window_w * 0.5), int(window_h * 0.5), text=int(score), font=TEXT_FONT, fill='white')
                    flag = False

                    print('data :'+score+',addr: {}',format(addr))
                    conn.sendall(b'Recived:'+data)

th = threading.Thread(name="a", target=print_num)
th.start()

root.mainloop()