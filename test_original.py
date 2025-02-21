import numpy as np
import cv2
import time
from cmath import phase
from math import degrees
import math
import cmath
import os
import pandas as pd

import sys
sys.path.append(os.path.abspath('yolov5'))
from BladeCapture import BladeCapture

# Grobal Preset
PCOM = 100      # Command Position Area
comx = 0        # X axis Command
comy = 0        # Y axis Command
comh = 0        # Z axis Command
size = 1.0      # BladeCapture Internal Size
offset = 10     # BladeCapture Internal Offset Value
qnum = 10000        # BladeCapture Internal Queue Size

# Camera Condition
mvw = 1920    # Movie Width (pixel)
mvh = 1080    # Movie Height (pixel)
fov = 145       # Movie Angular FoV (deg) - 水平
fr = 30         # Movie Frame (fps)
# Camera Position, Center = (0,0) (meter) こっち使ってる。これどうしようかな。
cp1 = (0.0, 0.2)  # Cam1 Position (meter)
cp2 = (-0.189, -0.1)       # Cam2 Position (meter)
cp3 = (0.189, -0.1)   # Cam3 Position (meter)
# Relative Distance (meter) 使ってない。
#d12 = 0.48               # Distance between Cam1 and Cam2
#d23 = 0.5               # Distance between Cam2 and Cam3
#d31 = 0.5               # Distance between Cam3 and Cam1
# Interneal Preset
#_ang = 2 * math.tan(fov*math.pi/360) / mvw
# Triangle Area Calculation (Cross Product)
def getArea(pts):
    xpts = np.array([pts[1][0]-pts[0][0],pts[1][1]-pts[0][1]])
    ypts = np.array([pts[2][0]-pts[0][0],pts[2][1]-pts[0][1]])
    #print(np.cross(xpts,ypts))
    return abs(np.cross(xpts,ypts))/2.0

def convAngle(p,off):
    return (np.deg2rad((p[0]+off[0]-mvw/2)*(fov/mvw)), np.deg2rad((p[1]+off[1]-mvh/2)*(fov/mvw)) )
    #return (math.atan(_ang * (p[0]+off[0] - mvw/2)), math.atan(_ang * (p[1]+off[1] - mvh/2)))

def aasTriangle(t1, t2, d12):# t3: angle disparity, d13
    t3 = t2 - t1
    if abs(math.sin(t3)) < 0.0001:
        t3 = 0.0001
    d13 = d12 * math.sin(math.pi/2 + t1) / math.sin(t3)
    d23 = d12 * math.sin(math.pi/2 - t2) / math.sin(t3)
    #print(t1, t2, d12, t3, d13, d23, math.sin(t3), math.sin(math.pi/2 + t1), math.sin(math.pi/2 - t2))
    #buf = input()
    return (t3, d13, d23)

# Precise Position Calculation
def getHeight(c1,c2,c3,o1,o2,o3):

    a1 = convAngle(c1,o1)
    a2 = convAngle(c2,o2)
    a3 = convAngle(c3,o3)
    # print(a1, a2, a3)

    # dc2 distance Calculate (X-Z)
#    (buf,dc12,buf) = aasTriangle(a2[0],a1[0],math.fabs(cp1[0]-cp2[0]))
#    (buf,dc32,buf) = aasTriangle(a2[0],a3[0],math.fabs(cp3[0]-cp2[0]))
    (buf,dc12x,buf) = aasTriangle(a1[0],a2[0],math.fabs(cp2[0]-cp1[0]))
    (buf,buf,dc13x) = aasTriangle(a3[0],a1[0],math.fabs(cp3[0]-cp1[0]))

    # dc2 distance Calculate (Y-Z)
#    (buf,buf,dc21) = aasTriangle(a1[1],a2[1],math.fabs(cp1[1]-cp2[1]))
#    (buf,dc23,buf) = aasTriangle(a2[1],a3[1],math.fabs(cp3[1]-cp2[1]))
    (buf,buf,dc12y) = aasTriangle(a2[1],a1[1],math.fabs(cp2[1]-cp1[1]))
    (buf,buf,dc13y) = aasTriangle(a3[1],a1[1],math.fabs(cp3[1]-cp1[1]))


    #print(dc21, dc23, dc12, dc32)
    # print(dc12x, dc13x, dc12y, dc13y)
    #print(a1[1]*180/math.pi,a2[1]*180/math.pi,a3[1]*180/math.pi)
    #print((math.sin(a2[1])*dc21, math.cos(a2[1])*dc21), (math.sin(a2[1])*dc23, math.cos(a2[1])*dc23))
    #print((math.sin(a2[0])*dc21-a2[0], math.cos(a2[0])*dc21), (math.sin(a2[0])*dc23-a2[0], math.cos(a2[0])*dc23))
    #xx = (math.sin(a2[0])*dc12 - o2[0] + math.sin(a2[0]) * dc32 - o2[0])/2
    #yy = (math.sin(a2[1])*dc21 - o2[1] + math.sin(a2[1]) * dc23 - o2[1])/2
    #hh = (math.cos(a2[1])*dc12+math.cos(a2[1])*dc32+math.cos(a2[1])*dc21+ math.cos(a2[1])*dc23)/4
    xx = (math.sin(a1[0])*dc12x - cp1[0] + math.sin(a1[0]) * dc13x - cp1[0])/2
    yy = (math.sin(a1[1])*dc12y - cp1[1] + math.sin(a1[1]) * dc13y - cp1[1])/2
    hh = (math.cos(a1[0])*dc12x + math.cos(a1[0])*dc13x+math.cos(a1[1])*dc12y+ math.cos(a1[1])*dc13y)/4
    # print((math.sin(a1[0])*dc12x - cp1[0] + math.sin(a1[0]) * dc13x - cp1[0])/2, (math.sin(a1[1])*dc12y - cp1[1] + math.sin(a1[1]) * dc13y - cp1[1])/2)
    # print(math.cos(a1[0])*dc12x, math.cos(a1[0])*dc13x, math.cos(a1[1])*dc12y, math.cos(a1[1])*dc13y)
    return (xx*100,yy*100,hh*100)

# Capture Setting (Hard Code)
#v1 = BladeCapture('C:\\Users\\yagu1\\Downloads\\frea\\frea\\20230207\\case01\\cam1.mp4',mvw,mvh,fr,size,offset,qnum,10240)
#v2 = BladeCapture('C:\\Users\\yagu1\\Downloads\\frea\\frea\\20230207\\case01\\cam2.mx2, y2p4',mvw,mvh,fr,size,offset,qnum,10200)
#v3 = BladeCapture('C:\\Users\\yagu1\\Downloads\\frea\\frea\\20230207\\case01\\cam3.mp4',mvw,mvh,fr,size,offset,qnum,10238)
v1 = BladeCapture('/home/iplslam/Husha/Data/test/dark_onigajo_case022_cam1.mp4',mvw,mvh,fr,size,offset,qnum,10)   # 変更箇所
v2 = BladeCapture('/home/iplslam/Husha/Data/test/dark_onigajo_case022_cam2.mp4',mvw,mvh,fr,size,offset,qnum,10)   # 変更箇所
v3 = BladeCapture('/home/iplslam/Husha/Data/test/dark_onigajo_case022_cam3.mp4',mvw,mvh,fr,size,offset,qnum,10)   # 変更箇所

# Capture Error Handling
if not v1.isOpened():
    raise RuntimeError("Error: V1 is not open")
if not v2.isOpened():
    raise RuntimeError("Error: V2 is not open")
if not v3.isOpened():
    raise RuntimeError("Error: V3 is not open")

# Center重心計算
c1, r1, l1 = v1.readset()
c2, r2, l2 = v2.readset()
c3, r3, l3 = v3.readset()

cc = ((1053,669), (1167,439), (834,390)) # Center Points
c1 = (1053,669)
c2 = (1167,439)
c3 = (834,390)
c1off = (-75,42)
c2off = (-25,39)
c3off = (6,82)
#cam1/contact : [1118,340]
#cam2/contact : [724,631]
#cam3/contact : [1144,850]
cm = tuple(map(lambda y: sum(y) / float(len(y)), zip(*cc))) # Gravity
pos = getHeight(c1,c2,c3,c1off,c2off,c3off) #高さ
cr = getArea(cc)

# Capture Start
v1.start()
v2.start()
v3.start()

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 1920, 1080)

path = r'/home/iplslam/Husha/test/movie/test_onigajo_case022_dark_original.mp4'   # 変更箇所
cap = cv2.VideoCapture(path)
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter(path, fmt, 29.7, (mvw,mvh))
cols_fps = ["throughput"]
df_throughput = pd.DataFrame(columns=cols_fps)
output_throughput = '/home/iplslam/Husha/test/original/case02_1/throughput_original.csv'     # 変更箇所

while True:
    os.system('cls')
    os.system('clear')
    # print("\033[9A", end="")
    # Cycle Time Calculation
    tim = time.time()
    # Extract Info
    ret1, frm1, t1 = v1.read()
    ret2, frm2, t2 = v2.read()
    ret3, frm3, t3 = v3.read()
    tim2 = time.time()
    # print("Main: ReadTime:", tim2 - tim)

    # Error Handling
    if not ret1 or not ret2 or not ret3:
        print ('Main: CAM ERROR')
        break
    # Center and Target Gravity Point Calculation
    tt = (t1, t2, t3)
    tm = tuple(map(lambda y: sum(y) / float(len(y)), zip(*tt)))
    ctx = cm[0]-tm[0]   # Disparity of x direction
    cty = cm[1]-tm[1]   # Disparity of y directionce
    # Get Height
    hhz = getHeight(c1,c2,c3,c1off,c2off,c3off)
    hh = getHeight(t1,t2,t3,c1off, c2off, c3off)
    # Get Area
    rr = getArea(tt)
    art = rr/cr
    # print("area rate: ", art)
    #cpos = (hh[0] - pos[0], hh[1] - pos[1], hh[2] - pos[2])
    # print("Main: ","x:", ctx, "  y:", cty)
    #print("Main: ","W:", cpos[0], " D:", cpos[1]," H:", cpos[2])
    # Control for drone
    if ctx < -PCOM:
        comx = 1       # Move Left
    elif ctx > PCOM:
        comx = -1        # Move Right
    else:
        comx = 0        # Keep Position
    if cty < -PCOM:
        comy = 1       # Move Forward
    elif cty > PCOM:
        comy = -1        # Move Back
    else:
        comy = 0        # Keep Position
    #if cpos[2] > 0.5:
    if art < 0.9:
        comh = 1        # Throttle Up
    #elif cpos[2] < -0.5:
    elif art > 1.1:
        comh = -1       # Throttle Down
    else:
        comh = 0        # Throttle Keep
    # print("Main: ", "Command:", comh, comx, comy)
    tim4 = time.time()

    #補正 === 2024/1/17更新
    ncm = np.array(cm)
    ntm = np.array(tm)
    mmm = math.cos(np.deg2rad((np.linalg.norm(ncm-ntm)/mvw)*fov))

    # Visualization
    frm4 = np.zeros(frm1.shape, dtype = np.uint8)
    #補正込みの表示  === 2024/1/17更新
    cv2.putText(frm4, "X:{0:.2f}cm, Y:{1:.2f}cm, H:{2:.2f}cm".format(hh[0]-pos[0], hh[1]-pos[1], (hh[2]-pos[2])*mmm), (50,50), cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,255), 1, cv2.LINE_AA)
    cv2.rectangle(frm4,(int(cm[0]/2-PCOM/2),int(cm[1]/2-PCOM/2)), (int(cm[0]/2+PCOM/2),int(cm[1]/2+PCOM/2)), (128,255,128), thickness=2)
    cv2.drawMarker(frm4, (int(cm[0]/2), int(cm[1]/2)), [128,255,128], markerType=cv2.MARKER_TILTED_CROSS, markerSize=8, thickness=2, line_type=cv2.LINE_8)
    cv2.drawMarker(frm4, (int(c1[0]/2)+c1off[0], int(c1[1]/2)+c1off[1]), [64,255,64], markerType=cv2.MARKER_TILTED_CROSS, markerSize=4, thickness=2, line_type=cv2.LINE_8)
    cv2.drawMarker(frm4, (int(c2[0]/2)+c2off[0], int(c2[1]/2)+c2off[1]), [64,255,64], markerType=cv2.MARKER_TILTED_CROSS, markerSize=4, thickness=2, line_type=cv2.LINE_8)
    cv2.drawMarker(frm4, (int(c3[0]/2)+c3off[0], int(c3[1]/2)+c3off[1]), [64,255,64], markerType=cv2.MARKER_TILTED_CROSS, markerSize=4, thickness=2, line_type=cv2.LINE_8)
    cv2.drawMarker(frm4, (int(t1[0]/2)+c1off[0], int(t1[1]/2)+c1off[1]), [128,64,255], markerType=cv2.MARKER_CROSS, markerSize=4, thickness=2, line_type=cv2.LINE_8)
    cv2.drawMarker(frm4, (int(t2[0]/2)+c2off[0], int(t2[1]/2)+c2off[1]), [64,128,255], markerType=cv2.MARKER_CROSS, markerSize=4, thickness=2, line_type=cv2.LINE_8)
    cv2.drawMarker(frm4, (int(t3[0]/2)+c3off[0], int(t3[1]/2)+c3off[1]), [64,64,255], markerType=cv2.MARKER_CROSS, markerSize=4, thickness=2, line_type=cv2.LINE_8)
    cv2.drawMarker(frm4, (int(tm[0]/2), int(tm[1]/2)), [128,128,255], markerType=cv2.MARKER_CROSS, markerSize=8, thickness=2, line_type=cv2.LINE_8)
    himg1 = np.hstack((frm4, frm1))
    himg2 = np.hstack((frm2, frm3))
    mImg = np.vstack((himg1, himg2))

    cv2.imshow('frame', cv2.resize(mImg,(mvw,mvh)))
    key = cv2.waitKey(int(1000/30))
    #cv2.imwrite(str(tim)+'_1.png', mImg)
    writer.write(cv2.resize(mImg,(mvw,mvh)))

    tim5 = time.time()
    # print("Main: VisualTime:", tim5 - tim4)

    if key == ord('q'):
        v1.loopflag = False
        v2.loopflag = False
        v3.loopflag = False
        time.sleep(1)
        v1.kill()
        v2.kill()
        v3.kill()
        break
    elif key == ord('z'):
        v1.loopflag = False
        v2.loopflag = False
        v3.loopflag = False
        time.sleep(1)
        v1.end()
        v2.end()
        v3.end()
        v1.gCutInit()
        v2.gCutInit()
        v3.gCutInit()
        v1.loopflag = True
        v2.loopflag = True
        v3.loopflag = True
        v1.start()
        v2.start()
        v3.start()
    # print("Main: Throughput - ",time.time()-tim)
    # new_record = [time.time()-tim]
    # df_throughput.loc[len(df_throughput)] = new_record
    # df_throughput.to_csv(output_throughput, index=False)

v1.release()
v2.release()
v3.release()
writer.release()
cv2.destroyAllWindows()
