import cv2
import numpy as np
from tqdm import tqdm

# コントラストと明るさを変更する関数
def adjust_contrast_brightness(image, alpha, beta):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

# 動画を読み込み
input_path = "/home/iplslam/Husha/Data/movie/1/onigajo_case02_2_cam2.mp4"
output_path = "/home/iplslam/Husha/Data/test/bright_onigajo_case022_cam2.mp4"

cap = cv2.VideoCapture(input_path)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# プログレスバーを表示
with tqdm(total=frame_count, desc="Processing Video", unit="frame") as pbar:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # コントラストと明るさの調整
        contrast = 1.5
        brightness = 50
        adjusted_frame = adjust_contrast_brightness(frame, contrast, brightness)

        # 調整したフレームを書き込み
        out.write(adjusted_frame)

        # プログレスバーを更新
        pbar.update(1)

        # 結果をリアルタイムで表示（オプション）
        cv2.imshow('Adjusted Video', adjusted_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
out.release()
cv2.destroyAllWindows()
