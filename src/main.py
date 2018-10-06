# coding: utf-8
'''
usage:
    keybind
    - esc: プログラムを終了
    - r: 赤色を選択
    - g: 緑色を選択
    - w: 白色を選択
    - b: 青色を選択
    - a: アタックチャンスモード
    - ,: １つ前の状態に戻す
    - .: リセット
    - t: シンキングタイムBGM再生
    - s: 正解BGM再生
    - m: 不正解BGM再生
    - q: 全サブPC早押しボタン点灯リセット
    - c: サジェスト機能の点灯リセット
    - S: 全BGM中断
'''

import socket
import tkinter as tk
from tkinter import messagebox
from time import sleep
import os
import threading
import pygame

# 表示サイズ
PANEL_SIZE = 140
PANEL_NUM = 5
TEXT_FONT = ('Calibre', PANEL_SIZE//2, ' bold')
# 色設定
DEFAULT_COLOR = "gray40"
ONCOLOR = "gray50"
ATTACK_CHANCE_COLOR = 'yellow'
colors = [
    "#FF001c", # 1-red
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
bg_color = 'gray70'
# チーム名設定
teams = []
try:
    f = open('team.txt', 'r')
    for line in f:
        team = line
        team = team.replace("\n","")
        team = team.replace("\r","")
        team = team.replace("\n\r","")
        teams.append(team)
    f.close()
except:
    teams = [1,2,3,4]

root = tk.Tk()
root.config(bg=bg_color)
CANVAS_W, CANVAS_H = root.winfo_screenwidth(), root.winfo_screenheight()
PANEL_RATE_W, PANEL_RATE_H = 0.8, 0.9
PANEL_W, PANEL_H = CANVAS_W * PANEL_RATE_W // PANEL_NUM, CANVAS_H * PANEL_RATE_H // PANEL_NUM
MARGIN_W = root.winfo_screenwidth() * (1. - PANEL_RATE_W) * 0.5
MARGIN_H = root.winfo_screenheight() * (1. - PANEL_RATE_H) * 0.5
CANVAS_SIZE = PANEL_W * PANEL_NUM  + MARGIN_W

# 効果音再生用ミキサー初期化
pygame.mixer.pre_init(frequency=48000, size = -16, channels = 2, buffer = 1024*4)
pygame.mixer.init()

# パネル点灯BGMの読み込み
sounds = []
sounds.append(pygame.mixer.Sound('../sounds/hayaoshi.wav'))
sounds.append(pygame.mixer.Sound('../sounds/gong.wav'))
sounds.append(pygame.mixer.Sound('../sounds/thinking.wav'))
sounds.append(pygame.mixer.Sound('../sounds/success.wav'))
sounds.append(pygame.mixer.Sound('../sounds/mistake.wav'))


# 色選択
colorselect = tk.IntVar()
colorselect.set(0)
rectangle_size = CANVAS_SIZE//teams.__len__()

keys = ['r', 'g', 'w', 'b']

#選択可能なパネルIDをpanels(list)に格納
def search(index):
    priority_1 = []
    priority_2 = []
    priority_3 = []
    # 8方向の探索用(右，右下，下，左下，左，左上，上)
    directs = [
        [ 1, 0 ], [ 1, 1 ], [ 0, 1 ], [-1, 1 ],
        [-1, 0 ], [-1, -1], [ 0, -1], [ 1, -1]
    ]
    #全パネルでループ
    for j in range(5):
        for i in range(5):
            judgenum = PANEL_NUM * j + i
            #もし選択されていないパネルならば
            if panelcolor[judgenum] == DEFAULT_COLOR or panelcolor[judgenum] == ATTACK_CHANCE_COLOR:
                #8方向でループ
                for h in range(8):
                    #端のパネルまで探索
                    x = i
                    y = j
                    cnt = 1
                    IS_SAME = False #探索先に同じ色があるか(優先順位１)
                    while True:
                        x += directs[h][0]
                        y += directs[h][1]
                        nownum = PANEL_NUM * y + x

                        if x < 0 or y < 0 or x >= 5 or y >= 5:
                            break

                        #隣が選択されていなければスキップ
                        if cnt == 1 and (panelcolor[nownum] == DEFAULT_COLOR or panelcolor[nownum] == ATTACK_CHANCE_COLOR):
                            break
                        #隣が自分と同じ色の場合 => 優先順位3
                        if cnt == 1 and panelcolor[nownum] == colors[index]:
                            if panelcolor[judgenum] == ATTACK_CHANCE_COLOR:
                                break
                            if not judgenum in priority_3:
                                priority_3.append(judgenum)
                            break
                        #間に別の色のパネルを挟んで空白に当たった場合 => 優先順位2
                        if cnt != 1 and (panelcolor[nownum] == DEFAULT_COLOR or panelcolor[nownum] == ATTACK_CHANCE_COLOR):
                            if not judgenum in priority_2 and panelcolor[judgenum] != ATTACK_CHANCE_COLOR:
                                priority_2.append(judgenum)
                            break
                        #間に別の色のパネルを挟んで同じ色に当たった場合 => 優先順位1
                        if cnt != 1 and panelcolor[nownum] == colors[index]:
                            if not judgenum in priority_1:
                                priority_1.append(judgenum)
                            IS_SAME = True
                            break
                        
                        cnt += 1
                    
                    if cnt != 1 and IS_SAME == False:
                        if not judgenum in priority_3 and panelcolor[judgenum] != ATTACK_CHANCE_COLOR:
                            priority_3.append(judgenum)

    #要素数0でない優先順位の高い配列を返す
    if priority_1.__len__() != 0:
        return priority_1
    elif priority_2.__len__() != 0:
        return priority_2
    elif priority_3.__len__() != 0:
        return priority_3
    else:
        return [12]

def reset_text(event):
    for n in range(PANEL_NUM**2):
        x = PANEL_W * (n%PANEL_NUM) + MARGIN_W
        y = PANEL_H * (n//PANEL_NUM) + MARGIN_H
        panel_label[n] = c0.create_text(x+(PANEL_W/2),y+(PANEL_H/2),text=str(n+1),font=TEXT_FONT, fill='black', activefill=ONCOLOR, tag='label')

#panelsのIDのパネルの文字を各色に点滅
def flash_text(panels, fillcolor):
    for n in panels:
        x = PANEL_W * (n%PANEL_NUM) + MARGIN_W
        y = PANEL_H * (n//PANEL_NUM) + MARGIN_H
        panel_label[n] = c0.create_text(x+(PANEL_W/2),y+(PANEL_H/2),text=str(n+1),font=TEXT_FONT, fill=fillcolor, activefill=ONCOLOR, tag='label')

swtch = False
def set_color(event):
    key = event.keysym
    idx = 0
    for k in keys:
        if key == k:
            colorselect.set(idx)
            break
        idx += 1
    #そのチームが選択可能なパネルを探索・点滅させる
    possible_panels = []
    possible_panels = search(idx)
    global swtch
    global pre_idx
    for i in range(3):
        reset_text(None)
        c0.update()
        sleep(0.25)
        flash_text(possible_panels, colors[idx])
        c0.update()
        sleep(0.25)
        swtch = True

for k in keys:
    root.bind("<"+ k +">", set_color)

# 盤面
c0 = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H, bg=bg_color, highlightthickness=0)
c0.grid(column=2,rowspan=teams.__len__())

panels = {}
panelcolor = {}
panel_label = {}
past_panelcolor = {}
scores = [0 for i in range(teams.__len__())]
is_attackchance_1 = False
is_attackchance_2 = False

SB_RATE_H = 0.6
SB_RATE_W = 0.7
SCORE_BOX_H = int(CANVAS_H * 0.9 * SB_RATE_H * 0.25)
SCORE_BOX_W = int(CANVAS_W * 0.1 * SB_RATE_W)

ip_adress = [
    '192.168.0.3', #赤
    '192.168.0.4', #緑
    '192.168.0.5', #白
    '192.168.0.6'  #青
]
fff = False # 早押し管理フラグ

# 得点更新
def rescore(event):
    sum_score = 0
    fff = False
    for i in range(teams.__len__()):
    #for i in range(1):
        count = 0
        for j in range(panelcolor.__len__()):
            if panelcolor[j] == colors[i]:
                count += 1
        sum_score += count
        scores[i] = count

        left_top_x = int(PANEL_W * PANEL_NUM + MARGIN_W + (1. - SB_RATE_W) * 0.5 * 0.1 * CANVAS_W)
        left_top_y = int(PANEL_H * (1. - SB_RATE_H) * PANEL_NUM + MARGIN_H)
        c0.create_rectangle(left_top_x, left_top_y + SCORE_BOX_H * i, left_top_x + SCORE_BOX_W, left_top_y + SCORE_BOX_H * i + SCORE_BOX_H, fill=colors[i], width=4)
        c0.create_text(int(left_top_x + SCORE_BOX_W * 0.5), int(left_top_y + SCORE_BOX_H * (i + 0.5)), text=count, font=TEXT_FONT, fill='black')
        
        # もしネットワーク通信による得点表示を使わない場合は以下をコメントアウトする
        '''
        #サーバとの通信
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # サーバを指定
            #s.connect((ip_adress[i], 50007))
            #s.connect(('127.0.0.1', 50007))
            #s.connect(('192.168.0.8', 50007))
            s.connect(('192.168.0.6', 50007))
            # サーバにメッセージを送る
            #num = str(count)
            num = str(scores[i])
            s.sendall(num.encode('utf-8'))
            # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
            data = s.recv(1024)
            print(repr(data))
        '''
        
    if sum_score == 20 and is_attackchance_2 == False:
        toggle_attackchance(None)
        

# 初期化
def reset(event):
    for n in range(PANEL_NUM ** 2):
        x = PANEL_W * (n%PANEL_NUM) + MARGIN_W
        y = PANEL_H * (n//PANEL_NUM) + MARGIN_H
        panels[n] = c0.create_rectangle(x, y, x+PANEL_W, y+PANEL_H, fill=DEFAULT_COLOR, activefill=ONCOLOR, tag='free', width=4)
        panelcolor[n] = DEFAULT_COLOR
        panel_label[n] = c0.create_text(x+(PANEL_W/2),y+(PANEL_H/2),text=str(n+1),font=TEXT_FONT, activefill=ONCOLOR, tag='label')

    rescore(None)

for n in range(PANEL_NUM ** 2):
        x = PANEL_W * (n%PANEL_NUM) + MARGIN_W
        y = PANEL_H * (n//PANEL_NUM) + MARGIN_H
        panels[n] = c0.create_rectangle(x, y, x+PANEL_W, y+PANEL_H, fill=DEFAULT_COLOR, activefill=ONCOLOR, tag='free', width=4)
        panelcolor[n] = DEFAULT_COLOR
        panel_label[n] = c0.create_text(x+(PANEL_W/2),y+(PANEL_H/2),text=str(n+1),font=TEXT_FONT, activefill=ONCOLOR, tag='label')

rescore(None)

# 選択したパネルのID取得
def find_items(id, items):
    for k,v in items.items():
        if v == id:
            return k

# オセロ
def reverse(color, color_id):
    selectedpanelid = c0.find_withtag("selected")[0]
    c0.itemconfigure(selectedpanelid, tag="filled")
    c0.itemconfigure("reverse", tag="filled", fill=color, activefill=color)
    c0.update()
    selectnum = find_items(selectedpanelid, panels)
    panelcolor[selectnum] = color
    
    # 8方向に探索(右，右下，下，左下，左，左上，上)
    directs = [
        [ 1, 0 ],
        [ 1, 1 ],
        [ 0, 1 ],
        [-1, 1 ],
        [-1, 0 ],
        [-1, -1],
        [ 0, -1],
        [ 1, -1]
    ]

    # 各探索方向に進む
    reversepanel = []
    start_x = selectnum % PANEL_NUM
    start_y = selectnum //PANEL_NUM
    for i in range(8):
        now_x = start_x
        now_y = start_y
        flag = False
        tmp = []
        while True:
            now_x += directs[i][0]
            now_y += directs[i][1]
            nownum = PANEL_NUM * now_y + now_x
            if now_x < 0 or now_y < 0 or now_x >= PANEL_NUM or now_y >= PANEL_NUM:
                break
            if panelcolor[nownum] == DEFAULT_COLOR:
                break
            if panelcolor[nownum] == color:
                flag = True
                break
            
            tmp.append(nownum)

        if flag == True:
            reversepanel.extend(tmp)
            
    for i in reversepanel:
        panelcolor[i] = color
        c0.itemconfigure(panels[i], tag="reverse")
        c0.itemconfigure("reverse", tag="filled", fill=color, activefill=color)
        c0.update()

        sounds[0].play()
        sleep(1)

    rescore(None)

# 塗り替え
def change_color(event):
    global is_attackchance_1
    global is_attackchance_2
    reset_text(None)
    backup()
    color_id = colorselect.get()

    sounds[0].play()

    aftercolor = colors[color_id]
    c0.itemconfigure('current', fill=aftercolor, tag='selected', activefill=aftercolor)
    c0.update()

    sleep(1)

    reverse(aftercolor, color_id)

    if is_attackchance_1:
        is_attackchance_1 = False
        is_attackchance_2 = True
    
# アタックチャンス
def set_attackchance(event):
    global is_attackchance_1
    global is_attackchance_2
    if is_attackchance_2:
        backup()
        c0.itemconfigure('current', fill=ATTACK_CHANCE_COLOR, tag='attack', activefill=ATTACK_CHANCE_COLOR)
        attackpanelid = c0.find_withtag('attack')[0]
        attackpanelnum = find_items(attackpanelid, panels)
        panelcolor[attackpanelnum] = ATTACK_CHANCE_COLOR
        rescore(None)
        c0.itemconfigure('attack', tag='free')
        is_attackchance_2 = False

c0.tag_bind('free', "<Button-1>", change_color)
c0.tag_bind('filled', "<Button-1>", set_attackchance)

# 得点表
c1 = tk.Canvas(root, width=10, height=10, bg='black', highlightthickness=0)
c1.grid(column=1, rowspan=teams.__len__())

scores_ = {}

# 初期表示
for i in range(teams.__len__()):
    if i < 10:
        color = colors[i]
    else:
        color = colors[i-10]
    left_top_x = int(PANEL_W * PANEL_NUM + MARGIN_W + (1. - SB_RATE_W) * 0.5 * 0.1 * CANVAS_W)
    left_top_y = int(PANEL_H * (1. - SB_RATE_H) * PANEL_NUM + MARGIN_H)
    c0.create_rectangle(left_top_x, left_top_y + SCORE_BOX_H * i, left_top_x + SCORE_BOX_W, left_top_y + SCORE_BOX_H * i + SCORE_BOX_H, fill=color, width=4)
    count = 0
    for j in range(panelcolor.__len__()):
        if panelcolor[j] == color:
            count += 1
    scores_[i] = c0.create_text(int(left_top_x + SCORE_BOX_W * 0.5), int(left_top_y + SCORE_BOX_H * (i + 0.5)), text=count, font=TEXT_FONT, fill='black')        
                                                                                                                                                                                                                                            
# アタックチャンス
def toggle_attackchance(event):
    global is_attackchance_1
    if is_attackchance_1:
        is_attackchance_1 = False
    else:
        popup_attackchance()
        is_attackchance_1 = True
        
def popup_attackchance():
    sounds[1].play() # 効果音再生
    messagebox.showinfo("ATTACK CHANCE !", "ATTACK CHANCE !")

# 一つ前に戻る
def back(event):
    if past_panelcolor == {}:
        return
    for n in panelcolor:
        if panelcolor[n] != past_panelcolor[n]:
            back_tag = 'filled'
            back_activefill = past_panelcolor[n]
            if past_panelcolor[n] == DEFAULT_COLOR:
                back_tag = 'free'
                back_activefill = ONCOLOR
            if past_panelcolor[n] == ATTACK_CHANCE_COLOR:
                back_tag='free'
            c0.itemconfigure(panels[n], tag=back_tag, fill=past_panelcolor[n], activefill=back_activefill)
            panelcolor[n] = past_panelcolor[n]
    rescore(None)

# バックアップをとる
def backup():
    for n in panelcolor:
        past_panelcolor[n] = panelcolor[n]

# 獲得枚数が最多の色のパネルid(0...24)を保存
def save_panel_num(event):
    for i in range(teams.__len__()):
        champ_panels = []

        path = "../datas/champ_panels" + str(i) + ".txt"
        for j in range(PANEL_NUM**2):
            if(panelcolor[j] == colors[i]):
                champ_panels.append(j)

        with open(path, mode='w') as f:
            for e in champ_panels:
                f.write(str(e) + '\n')
    event.widget.quit()

def play_music(event):
    if event.keysym == 't':
        sounds[2].play()
    elif event.keysym == 's':
        sounds[3].play()
    elif event.keysym == 'm':
        sounds[4].play()

def stop_music(event):
    for s in sounds:
        s.stop()

# 'a'キー入力でアタックチャンス発動
root.bind("<a>", toggle_attackchance)
# 戻るボタン
root.bind("<,>", back)
# リセットボタン
root.bind("<.>", reset)
# 文字色リセットボタン
root.bind("<c>", reset_text)
# 早押しセッションリセットボタン
root.bind("<q>", rescore)
# シンキングタイムBGM
root.bind("<t>", play_music)
# 正解BGM
root.bind("<s>", play_music)
# 不正解BGM
root.bind("<m>", play_music)
# 全サウンド停止
root.bind("<S>", stop_music)
# フルスクリーン＆キーバインド
root.overrideredirect(True)
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.overrideredirect(False)
root.bind("<Escape>", save_panel_num)



# 別スレッドでメッセージの受信を行う関数
def stand_by():
    global fff
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
        #sc.bind(('192.168.0.2',50007))
        sc.bind(('192.168.0.12',50007))
        sc.listen(1)

        while True:
            conn,addr = sc.accept()
            with conn:

                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # 最も早い回答者IDを取得
                    contestant_id = int(data.decode('utf-8'))

                    print('Fastest ID :'+ contestant_id +',addr: {}',format(addr))
                    if fff == False:
                        fff = True
                        judge = '1'
                    else:
                        judge = '0'
                    conn.sendall(judge.encode('utf-8'))

# 早押し機能を使わない場合以下2行をコメントアウト
'''
th = threading.Thread(name="stand_by", target=stand_by)
th.start()
'''


root.mainloop()
