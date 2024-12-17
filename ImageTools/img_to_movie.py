import cv2
import os
from tqdm import tqdm  # プログレスバー用ライブラリ

# 入力画像ディレクトリ
input_dir = "/home/iplslam/Husha/Data/Yolo_images/20230907/cam3/blade_images_with_points"  # 点が描画された画像のディレクトリ
output_video_path = "/home/iplslam/Husha/Data/Yolo_images/20230907/cam3/output_video.mp4"  # 出力する動画のパス

# 動画設定
frame_rate = 10  # フレームレート（例: 10fps）
output_frame_size = (640, 480)  # 出力動画のフレームサイズ（幅, 高さ）

# 画像ファイルの一覧を取得しソート
image_files = sorted([f for f in os.listdir(input_dir) if f.endswith(('.jpg', '.png'))])

if not image_files:
    print("No images found in the directory.")
    exit()

# 動画ライターを作成
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # コーデック（MP4用: 'mp4v' または 'avc1'）
out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, output_frame_size)

# 各画像をフレームとして動画に追加（プログレスバーを表示）
for image_file in tqdm(image_files, desc="Processing images", unit="frame"):
    image_path = os.path.join(input_dir, image_file)
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to read image: {image_path}")
        continue
    
    # 画像を統一サイズにリサイズ
    resized_img = cv2.resize(img, output_frame_size)
    
    # 動画にフレームを追加
    out.write(resized_img)

# 動画ライターを解放
out.release()
print(f"Video saved at: {output_video_path}")
