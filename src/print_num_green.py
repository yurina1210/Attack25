import socket
import cv2
import numpy as np

score = str(0)
cv2.namedWindow("num", cv2.WINDOW_NORMAL)
cv2.setWindowProperty('num', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
path = '../numbers/0.png'

print(path)
img = cv2.imread(path)

cv2.imshow('num', img)

cv2.waitKey(1)
        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #s.bind(('192.168.0.4',50007))
    s.bind(('127.0.0.1',50007))
    s.listen(1)

    while True:
        path = '../numbers/' + score + '.png'
        print(path)
        img = cv2.imread(path)

        edge_wide = 40
        h, w = img.shape[:2]
        for j in range(h):
            for i in range(w):
                if ((i >= 0 and i < edge_wide) or (i >= w - edge_wide and i < w)) \
                or ((j >= 0 and j < edge_wide) or (j >= h - edge_wide and j < h)):
                    img.itemset((j,i,0),34)
                    img.itemset((j,i,1),139)
                    img.itemset((j,i,2),34)

        cv2.imshow('num', img)
        
        key = cv2.waitKey(1)&0xff
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit()

        
        conn,addr = s.accept()
        with conn:

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                score = data.decode('utf-8')

                print('data :'+score+',addr: {}',format(addr))
                conn.sendall(b'Recived:'+data)

                if key == ord('q'):
                    cv2.destroyAllWindows()
                    exit()

        
        
                