import pandas as pd
import cv2
import os
from tqdm import tqdm

# 入力ディレクトリとファイルパス
base_dir = "/home/iplslam/Husha/test/original/case02_1/cam1"
csv_path = os.path.join(base_dir, "cam1.csv")
images_dir = os.path.join(base_dir, "blade_images")
output_dir = os.path.join(base_dir, "blade_images_with_points") 
output_csv_path = os.path.join(base_dir, "processed_points_whole.csv")  # 保存するCSVファイルのパス

# 出力ディレクトリを作成
os.makedirs(output_dir, exist_ok=True)

# CSVを読み込む
df = pd.read_csv(csv_path)

# 結果を保存するためのリスト
results = []

# CSVをループして対応する画像に点を描画（プログレスバー付き）
for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing images", unit="frame"):
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

    x1 = int(row["Frame_left"])
    y1 = int(row["Frame_top"])
    x2 = int(row["Frame_right"])
    y2 = int(row["Frame_bottom"])
    
    # Tip_x, Tip_yの座標を取得
    tip_x = int(row["Tip_x"]) - x1
    tip_y = int(row["Tip_y"]) - y1

    # 補正
    rectangle_x1 = int(tip_x - 30)
    rectangle_y1 = int(tip_y - 40)
    rectangle_x2 = tip_x + 10
    rectangle_y2 = tip_y + 0

    # 点を描画（赤い円）
    color = (0, 0, 255)  # BGR形式（赤色）
    radius = 5  # 半径
    thickness = -1  # 塗りつぶし
    # cv2.circle(img, (tip_x, tip_y), radius, color, thickness)
    cv2.rectangle(img, (rectangle_x1, rectangle_y1), (rectangle_x2, rectangle_y2), (255, 0, 0), 2)
    
    # 描画した画像を保存
    output_path = os.path.join(output_dir, image_name)
    cv2.imwrite(output_path, img)

    # 結果を保存するリストに追加
    results.append({
        "Tip_x": tip_x,
        "Tip_y": tip_y,
        "Rectangle_x1": rectangle_x1,
        "Rectangle_y1": rectangle_y1,
        "Rectangle_x2": rectangle_x2,
        "Rectangle_y2": rectangle_y2
    })

# DataFrameに変換してCSVに保存
results_df = pd.DataFrame(results)
results_df.to_csv(output_csv_path, index=False)
print(f"Results saved to: {output_csv_path}")
