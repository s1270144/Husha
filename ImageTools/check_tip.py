import pandas as pd
import cv2
import os

# 入力ディレクトリとファイルパス
base_dir = "/home/iplslam/Husha/Data/Yolo_images/20230907/cam1"
csv_path = os.path.join(base_dir, "cam1.csv")
images_dir = os.path.join(base_dir, "blade_images")
output_dir = os.path.join(base_dir, "blade_images_with_points") 

# 出力ディレクトリを作成
os.makedirs(output_dir, exist_ok=True)

# CSVを読み込む
df = pd.read_csv(csv_path)

# CSVをループして対応する画像に点を描画
for idx, row in df.iterrows():
    # 対応する画像ファイル名を取得
    image_name = f"frame_{idx}.jpg"  # インデックスに対応する画像名
    image_path = os.path.join(images_dir, image_name)
    
    # 画像が存在しない場合はスキップ
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        continue
    
    # 画像を読み込む
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to read image: {image_path}")
        continue

    height, width, channels = img.shape
    print(f"Image size for {image_name}: Width={width}, Height={height}, Channels={channels}")

    x1 = int(row["Frame_left"])
    y1 = int(row["Frame_top"])
    x2 = int(row["Frame_right"])
    y2 = int(row["Frame_bottom"])
    
    # Tip_x, Tip_yの座標を取得
    tip_x = int(row["Tip_x"]) - x1
    tip_y = int(row["Tip_y"]) - y1

    print(tip_x, tip_y)
    
    # 点を描画（赤い円）
    color = (0, 0, 255)  # BGR形式（赤色）
    radius = 5  # 半径
    thickness = -1  # 塗りつぶし
    cv2.circle(img, (tip_x, tip_y), radius, color, thickness)
    
    # 描画した画像を保存
    output_path = os.path.join(output_dir, image_name)
    cv2.imwrite(output_path, img)

    print(f"Processed and saved: {output_path}")
