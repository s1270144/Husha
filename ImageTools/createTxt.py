import csv
import os
import cv2  # OpenCVを利用して画像サイズを取得

# 入力ディレクトリと出力ディレクトリのパス
input_dir = '/home/iplslam/Husha/test/original/trimmed/cam3/'
output_dir = input_dir

# csvが格納されているパス
input_csv_file = os.path.join(input_dir, "processed_points.csv")

# 画像が格納されているディレクトリ
image_dir = os.path.join(input_dir, "blade_images_with_points")

# 出力ディレクトリを作成
output_subdir = os.path.join(output_dir, os.path.splitext(os.path.basename(input_csv_file))[0])
os.makedirs(output_subdir, exist_ok=True)

# CSVファイルを読み込む
with open(input_csv_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        # 画像ファイル名を推定
        image_name = f"frame_{i}.jpg"
        image_path = os.path.join(image_dir, image_name)  # 指定された画像ディレクトリ
        
        # 画像が存在しない場合はスキップ
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            continue
        
        # 画像サイズを取得
        img = cv2.imread(image_path)
        if img is None:
            print(f"Failed to read image: {image_path}")
            continue
        image_height, image_width, _ = img.shape
        
        # 各行のRectangle_x1, Rectangle_y1, Rectangle_x2, Rectangle_y2の値を取得
        frame_left = int(row['Rectangle_x1'])
        frame_top = int(row['Rectangle_y1'])
        frame_right = int(row['Rectangle_x2'])
        frame_bottom = int(row['Rectangle_y2'])
        
        # 中心座標と幅、高さを計算
        center_x = (frame_left + frame_right) / 2.0
        center_y = (frame_top + frame_bottom) / 2.0
        width = frame_right - frame_left
        height = frame_bottom - frame_top
        
        # 座標を正規化
        center_x /= image_width
        center_y /= image_height
        width /= image_width
        height /= image_height
        
        # 出力テキストファイルの名前を作成
        output_txt_file = os.path.join(output_subdir, f'frame_{i}.txt')
        
        # クラスIDは仮に0として、YOLO形式で書き込む
        with open(output_txt_file, 'w') as txtfile:
            txtfile.write(f"0 {center_x} {center_y} {width} {height}")

print("ファイルの書き込みが完了しました。")
