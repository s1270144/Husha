import threading
import queue
import numpy as np
import cv2
import time
import sys
import math
import os
import torch
from collections import deque
from matplotlib import pyplot as plt
import pandas as pd
from PIL import Image

class BladeCapture():

    # Primitive Color
    CR_RECT = [255,0,0]     # rectangle color
    CR_CENT = [64,172,0]    # Center Pole Position
    CR_CAMR = [172,0,64]    # Right Camera Position
    CR_CAML = [0,64,172]    # Left Camera Position
    CR_FG = [0,255,0]       # Sure FG
    CR_BG = [0,0,255]       # Sure BG
    CR_PFG = [193,193,193]  # Prob FG
    CR_PBG = [31,31,31]     # Prob BG

    # Region Color Definition
    DRAW_BG = {'color' : CR_BG, 'val' : 0}
    DRAW_FG = {'color' : CR_FG, 'val' : 1}
    DRAW_PR_BG = {'color' : CR_PBG, 'val' : 2}
    DRAW_PR_FG = {'color' : CR_PFG, 'val' : 3}

    # Global Variables
    src = None                      # Source File or Camera ID
    video = None                    # Videocapture
    fourcc = None                   # FourCC
    width, height, fps = 1920, 1080, 30 # Video width, height, fps
    rect = (0,0,0,0)                # Target Rectangle
    offset = 10                     # Target rectangle offset
    point = [0,0,0,0]               # Target Point
    center = (0,540)                  # Image Center
    cppos = (0,0)                   # UAV Center Pole Position
    rcpos = (0,0)                   # Right Camera Position
    lcpos = (0,0)                   # Left Camera Position
    tgtpnt = (0,0)                  # Blade Target
    pretgtpnt = (0,0)
    size = 1.0                      # Image Shrinking
    thickness = 5                   # Mask Drawing Thckness
    q, p = None, None               # q: Image buffer, p: Target point buffer
    qq, pp = None, None               # q: Image buffer, p: Target point buffer
    ix, iy = 0, 0                   # Mouse
    xx, yy = [0,0], [0,0]           # left, right, top, bottom bounds of boundary
    x1_f, y1_f, x2_f, y2_f = 0, 0, 0, 0
    x1_t, y1_t, x2_t, y2_t = 0, 0, 0, 0
    loopflag = True
    errorCntShrink = 0
    errorCnt = 0
    resizeFlag = True
    cols = ["Tip_x", "Tip_y", "Frame_left", "Frame_top", "Frame_right", "Frame_bottom", 'cam']
    df = pd.DataFrame(columns=cols)
    output_dir = '/home/iplslam/Husha/test/yolo/case02_2'
    weights_path_f = '/home/iplslam/Husha/yolov5/runs/train/BladeFrame/weights/best.pt'
    weights_path_t = '/home/iplslam/Husha/yolov5/runs/train/BladeTip/weights/best.pt'
    device = 'cuda'
    model_f = torch.hub.load('/home/iplslam/Husha/yolov5', 'custom', path=weights_path_f, source='local')
    model_f.to(device)
    model_f.eval()
    model_t = torch.hub.load('/home/iplslam/Husha/yolov5', 'custom', path=weights_path_t, source='local')
    model_t.to(device)
    model_t.eval()
    resized_width = 640
    resized_height = 640
    scale_x = resized_width / width
    scale_y = resized_height / height
    # target = (1920, 1080)
    target = (0, 0)
    # target = (0, 1080)
    # target = (1920, 0)
    # Image Buffers
    #img, img2, mask, out, cont, nimg, nmsk = None, None, None, None, None, None, None

    # Global flags
    _value = DRAW_FG                # Drawing
    _drawingMask = False            # Mask drawing
    _drawingRect = False            # Target rectangle drawing
    _enableRect = False             # Rectangle drawed
    _enableMask = -1                # Mask drawed
    _mode = 1                       #
    _stopped = False                #
    _routine = False                # Setup or _routine

    # Class Initialization
    def __init__(self, src, width=1920, height=1080, fps=15, size=1.0, offset=10,max_queue_size=8, fshift=0):
        # Sourse Definition (capture ID, resource)
        self.src = src
        self.fps = fps
        self.mq = max_queue_size
        # Capture Setting
        self.video = cv2.VideoCapture(src)
        self.video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.video.set(cv2.CAP_PROP_FPS, fps)
        self.video.set(0,fshift*(1000/fps))
        # Capture Setting Refrection
        self.fourcc = self.decode_fourcc(self.video.get(cv2.CAP_PROP_FOURCC))
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        # Process Setting
        self.size = size
        self.offset = offset
        self.center = (int(width*size/2),int(height*size/2))
        #print(self.center)
        self.qq = deque(maxlen=1)
        self.pp = deque(maxlen=1)
        self.q = queue.Queue(maxsize=max_queue_size)
        self.p = queue.Queue(maxsize=max_queue_size)
        # Class Inner Value Setting
        self._stopped = False
        self._mode = 1
        # Output
        self.output_dir = os.path.join(self.output_dir, f'{os.path.splitext(os.path.basename(self.src))[0]}')
        self.output_whole_img_dir = os.path.abspath(os.path.join(self.output_dir, f'whole_images'), )
        self.output_blade_img_dir = os.path.abspath(os.path.join(self.output_dir, f'blade_images'))
        os.makedirs(self.output_whole_img_dir, exist_ok=True)
        os.makedirs(self.output_blade_img_dir, exist_ok=True)
        self.frame_cnt = 0
        # Grubcut Initialization
        self.gCutInit()

    ###
    # FourCC Decoding from Video Capture
    def decode_fourcc(self,v):
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

    ###
    # Mouse Interface
    def onmouse(self, event, x, y, flags, param):

        # Pointing center pole position
        if self._mode == 0:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.cppos = (x,y)
                self.img = self.img2.copy()
                cv2.drawMarker(self.img, self.cppos, self.CR_CENT, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                cv2.drawMarker(self.img, self.rcpos, self.CR_CAMR, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                cv2.drawMarker(self.img, self.lcpos, self.CR_CAML, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                cv2.rectangle(self.img, (self.rect[0], self.rect[1]), (self.rect[0]+self.rect[2], self.rect[1]+self.rect[3]), self.CR_RECT, 2)
                ### Todo - Draw mask ###

        # Pointing right camera position
        elif self._mode == 3:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.rcpos = (x,y)
                self.img = self.img2.copy()
                cv2.drawMarker(self.img, self.cppos, self.CR_CENT, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                cv2.drawMarker(self.img, self.rcpos, self.CR_CAMR, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                cv2.drawMarker(self.img, self.lcpos, self.CR_CAML, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                cv2.rectangle(self.img, (self.rect[0], self.rect[1]), (self.rect[0]+self.rect[2], self.rect[1]+self.rect[3]), self.CR_RECT, 2)
                ### Todo - Draw mask ###

        # Pointing right camera position
        elif self._mode == 4:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.lcpos = (x,y)
                self.img = self.img2.copy()
                cv2.drawMarker(self.img, self.cppos, self.CR_CENT, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                cv2.drawMarker(self.img, self.rcpos, self.CR_CAMR, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                cv2.drawMarker(self.img, self.lcpos, self.CR_CAML, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                cv2.rectangle(self.img, (self.rect[0], self.rect[1]), (self.rect[0]+self.rect[2], self.rect[1]+self.rect[3]), self.CR_RECT, 2)
                ### Todo - Draw mask ###

        # Drawing target rectangle
        elif self._mode == 1:
            if event == cv2.EVENT_LBUTTONDOWN:
                self._drawingRect = True
                self.ix, self.iy = x,y
                self.point[0], self.point[1] = self.ix, self.iy
                cv2.drawMarker(self.img, self.cppos, self.CR_CENT, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                cv2.drawMarker(self.img, self.rcpos, self.CR_CAMR, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                cv2.drawMarker(self.img, self.lcpos, self.CR_CAML, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
            elif event == cv2.EVENT_MOUSEMOVE:
                if self._drawingRect == True:
                    self.img = self.img2.copy()
                    cv2.drawMarker(self.img, self.cppos, self.CR_CENT, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                    cv2.drawMarker(self.img, self.rcpos, self.CR_CAMR, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                    cv2.drawMarker(self.img, self.lcpos, self.CR_CAML, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                    cv2.rectangle(self.img, (self.ix, self.iy), (x, y), self.CR_RECT, 2)
                    self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
                    self._enableMask = 0
            elif event == cv2.EVENT_LBUTTONUP:
                if self._drawingRect:
                    self._drawingRect = False
                    self._enableRect = True
                    self.point[2], self.point[3] = x, y
                    cv2.drawMarker(self.img, self.cppos, self.CR_CENT, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                    cv2.drawMarker(self.img, self.rcpos, self.CR_CAMR, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                    cv2.drawMarker(self.img, self.lcpos, self.CR_CAML, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
                    cv2.rectangle(self.img, (self.ix, self.iy), (x, y), self.CR_RECT, 2)
                    self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
                    self._enableMask = False
                    self.pimg = self.img[self.rect[1]:self.rect[1]+self.rect[3],self.rect[0]:self.rect[0]+self.rect[2],:]
                    self.pmask = self.pimg[:,:,0]
                    print(" Now press the key 'n' a few times until no further change \n")

        # Draw Touchup Curves
        elif self._mode == 2:
            if event == cv2.EVENT_LBUTTONDOWN:
                self._drawingMask = True
                cv2.circle(self.img, (x,y), self.thickness, self._value['color'], -1)
                cv2.circle(self.mask, (x,y), self.thickness, self._value['color'], -1)
            elif event == cv2.EVENT_MOUSEMOVE:
                if self._drawingMask:
                    cv2.circle(self.img, (x, y), self.thickness, self._value['color'], -1)
                    cv2.circle(self.mask, (x, y), self.thickness, self._value['color'], -1)
            elif event == cv2.EVENT_LBUTTONUP:
                if self._drawingMask:
                    self._drawingMask = False
                    self._enableMask = True
                    cv2.circle(self.img, (x, y), self.thickness, self._value['color'], -1)
                    cv2.circle(self.mask, (x, y), self.thickness, self._value['color'], -1)
        # Else: Nothing
        else:
            None

    #=====================================
    # graphCut Method
    # - We should not share the global variable here
    # img:
    def graphCut(self, img):
        
        # Detection surrounding rectangle with Yolo
        try:
            img_sub = Image.fromarray(img)
            results = self.model_f(img_sub)
            coordinates = results.xyxy[0].cpu().numpy()
            columns = ['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class']
            df_f = pd.DataFrame(coordinates, columns=columns)
            # print(df_f)
            self.x1_f = int(df_f['xmin'][0])
            self.y1_f = int(df_f['ymin'][0])
            self.x2_f = int(df_f['xmax'][0])
            self.y2_f = int(df_f['ymax'][0])
            self.pimg = self.img[self.y1_f:self.y2_f, self.x1_f:self.x2_f, :] # Inside surrounding frame        
            cv2.rectangle(self.img, (self.x1_f, self.y1_f), (self.x2_f, self.y2_f), self.CR_RECT, 2)
        except:
            print("ERROR_IN_DETECTION_BLADE")
            import traceback
            traceback.print_exc()

        # Detection blade's tip with Yolo
        try:
            img_sub = Image.fromarray(self.pimg)
            results = self.model_t(img_sub)
            coordinates = results.xyxy[0].cpu().numpy()
            columns = ['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class']
            df_t = pd.DataFrame(coordinates, columns=columns)
            # print(df_t)
            self.x1_t = int(df_t['xmin'][0]) + self.x1_f
            self.y1_t = int(df_t['ymin'][0]) + self.y1_f
            self.x2_t = int(df_t['xmax'][0]) + self.x1_f
            self.y2_t = int(df_t['ymax'][0]) + self.y1_f
            self.tgtpnt = (int((self.x1_t + self.x2_t) / 2), int((self.y1_t + self.y2_t) / 2))
            cv2.rectangle(self.img, (self.x1_t, self.y1_t), (self.x2_t, self.y2_t), self.CR_RECT, 2)
            cv2.circle(self.img, self.tgtpnt, 5, (0, 0, 255), -1, 8, 0)
        except:
            print("ERROR_IN_DETECTION_TIP")
            import traceback
            traceback.print_exc()

        # write csv file
        # new_record = [self.tgtpnt['X'], self.tgtpnt['Y'], self.x1, self.y1, self.x2, self.y2, os.path.splitext(os.path.basename(self.src))[0]]
        # self.df.loc[len(self.df)] = new_record
        # self.df.to_csv(os.path.join(self.output_dir, f"Tip.csv"), index=False)

        # Whole image
        cv2.imwrite(os.path.join(self.output_whole_img_dir, f"frame_{self.frame_cnt}.jpg"), self.img)

        # Crop the image
        cv2.imwrite(os.path.join(self.output_blade_img_dir, f"frame_{self.frame_cnt}.jpg"), self.pimg)

        self.frame_cnt += 1


    #==================================
    # gCutInit: グラブカットの初期設定値を収集する
    # - 基本的に初期設定値はクラスGlobal変数に格納しておきたい
    # 初期設定値として必要なもの
    #  > 初期マスク画像 (FG: CR_CENT(0,255,0), BG: CR_BG (0,0,255), PR_FG: (255,127,63), PR_BG: (31,31,31))
    #   - マスクへの変換: 3番目が 0, 255, 63, 31になるので、それぞれ 1, 0, 3, 2にgraphCut内で変換
    #  > 初期領域 (rect: x1, y1, w, h)
    #   - 使用領域への変換: カットする場所はx1,y1,x1+w-1, y1+h-1になる
    #  > ターゲットマストの付け根位置 (x,y)
    #  > 他の２つのカメラ位置 (x1, y1), (x2, y2) -> 時計周りに指定
    def gCutInit(self):
        # 初期設定値終了フラグ
        self._routine = False;
        self._enableRect = True;
        while True:
            ret, img = self.video.read() # read a shot
            self.img = img.copy()                                    #Visualize Buffer
            self.img2 = img.copy()                                   # Working Buffer
            self.mask = np.zeros(self.img.shape, dtype = np.uint8)   # Mask Buffer (CR_PBG)
            self.out = np.zeros(self.img.shape, dtype = np.uint8)    # Output Buffer
            self.cont = np.zeros(self.img.shape, dtype = np.uint8)   # Contour Image Buffer
            # Windows Definition
            cv2.namedWindow('input',cv2.WINDOW_GUI_NORMAL)
            cv2.setMouseCallback('input', self.onmouse)
            cv2.moveWindow('input', 80,10)
            cv2.resizeWindow('input', 1920, 1080)

            # Local Variable Initialization

            cv2.drawMarker(self.img, self.cppos, self.CR_CENT, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
            cv2.drawMarker(self.img, self.rcpos, self.CR_CAMR, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)
            cv2.drawMarker(self.img, self.lcpos, self.CR_CAML, markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2, line_type=cv2.LINE_8)

            # Help Indicate
            print(" Instructions: \n")
            print(" Draw a rectangle around the object using right mouse button \n")

            while(1):
                # View input and output images
                cv2.imshow('input', self.img)

                k = cv2.waitKey(10)
                # key bindings [ESC,0,1,2,3,4,r,n]
                if k == 27:         # esc to exit
                    self._routine = True;
                    # print(self._routine, self._mode, self._enableMask, self._enableRect)
                    cv2.destroyAllWindows()
                    return
                elif k == ord('1'): # BG drawing
                    if(self._enableRect):
                        print(" mark background regions with left mouse button \n")
                        self._mode = 2
                        self._value = self.DRAW_BG
                    else:
                        print(" Mark interest region first.\n")
                elif k == ord('2'): # FG drawing
                    if(self._enableRect):
                        print(" mark foreground regions with left mouse button \n")
                        self._mode = 2
                        self._value = self.DRAW_FG
                    else:
                        print(" Mark interest region first.\n")
                elif k == ord('3'): # PR_BG drawing
                    if(self._enableRect):
                        print(" Mark PROBABLY background regions with left mouse button \n")
                        self._mode = 2
                        self._value = self.DRAW_PR_BG
                    else:
                        print(" Mark interest region first.\n")
                elif k == ord('4'): # PR_FG drawing
                    if(self._enableRect):
                        print(" mark PROBABLY foreground regions with left mouse button \n")
                        self._mode = 2
                        self._value = self.DRAW_PR_FG
                    else:
                        print(" Mark interest region first.\n")
                elif k == ord('c'): # center pole pointing
                    if(self._enableRect):
                        print(" point the top of center pole of the drone \n")
                        self._mode = 0
                    else:
                        print(" Mark interest region first.\n")
                elif k == ord('r'): # right camera pointing
                    if(self._enableRect):
                        print(" point the left camera position of the drone \n")
                        self._mode = 3
                    else:
                        print(" Mark interest region first.\n")
                elif k == ord('l'): # left camera pointing
                    if(self._enableRect):
                        print(" point the right camera position of the drone \n")
                        self._mode = 4
                    else:
                        print(" Mark interest region first.\n")
                elif k == ord('a'): # reset everything and get current frame
                    print("resetting and get current frame\n")
                    self._mode = 1
                    self.point = [0,0,0,0]
                    flag = 0
                    self._drawingRect = False
                    self._drawingMask = False
                    self._enableRect = False
                    self._enableMask = -1
                    self._value = self.DRAW_FG
                    break # restart this function
                elif k == ord('n'): # segment the image
                    print(""" For finer touchups, mark foreground and background after pressing keys 0-4
                    and again press 'n' \n""")
                    try:
                        self.graphCut(self.img2)
                    except:
                        print("ERROR_IN_GCUTINIT")
                        import traceback
                        traceback.print_exc()

    def start(self):
        self.started = threading.Event()
        self.thread = threading.Thread(target=self.update )
        self._stopped = False
        self.thread.start()
        return self

    def begin(self):
        self.loopflag = True
        self.started.set()

    def end(self):
        self.started.clear()
        print("\nend")

    def kill(self):
        self.started.set()
        self._stopped = False
        self.thread.join()

    def update(self):
        # Start Thread
        self.qq = deque(maxlen=1)
        self.pp = deque(maxlen=1)
        self.q = queue.Queue(maxsize=self.mq)
        self.p = queue.Queue(maxsize=self.mq)
        while self.loopflag:
            ctime = time.time()
            # Thread Stop
            if self._stopped:
                return
            # get a Image
            ret, img = self.video.read()

            # if there is no image: stop
            if not ret:
                self.stop()
                return
            # Visualize Buffer
            self.img = img.copy()
            try:
                self.graphCut(img)
            except:
                print("ERROR_IN_UPDATE")
                import traceback
                traceback.print_exc()
                #cv2.destroyAllWindows()
                #self.gCutInit()
            if self.q.full():
                self.q.get()
                self.p.get()
            self.q.put((ret, cv2.resize(self.img,(960,540)), ctime))
            self.p.put((self.tgtpnt, ctime))
        self.started.wait()

    def readset(self):
        return(self.cppos, self.rcpos, self.lcpos)

    def read(self):
        #ret, frm, tim = self.qq.pop()
        #tgtpnt, tim2 = self.pp.pop()
        ret, frm, tim = self.q.get()
        tgtpnt, tim2 = self.p.get()
        err = time.time() - tim
        # print("readTime ", self.src, ":", err)
        return (ret,frm,tgtpnt)

    def stop(self):
        self._stopped = True

    def release(self):
        self._stopped = True
        self.video.release()

    def isOpened(self):
        return self.video.isOpened()

    def get(self,i):
        return self.video.get(i)

    def join(self):
        self.thread.join()
