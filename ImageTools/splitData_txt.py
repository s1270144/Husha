import os
import shutil
import random

# 指定されたフォルダのパス
image_all_data_folder = '/home/iplslam/Husha/Dataset/Yolo_images/jpg'
txt_all_data_folder = '/home/iplslam/Husha/Dataset/Yolo_images/txt'

# Output
train_img_path = '/home/iplslam/Husha/Dataset/Yolo_images/images_t'
train_txt_path = '/home/iplslam/Husha/Dataset/Yolo_images/labels_t'
valid_img_path = '/home/iplslam/Husha/Dataset/Yolo_images/images_v'
valid_txt_path = '/home/iplslam/Husha/Dataset/Yolo_images/labels_v'
os.makedirs(train_img_path, exist_ok=True)
os.makedirs(train_txt_path, exist_ok=True)
os.makedirs(valid_img_path, exist_ok=True)
os.makedirs(valid_txt_path, exist_ok=True)

# ファイルのリストを取得し、拡張子を除いた名前でソート
image_files = sorted([f for f in os.listdir(image_all_data_folder) if f.endswith('.jpg')])
txt_files = sorted([f for f in os.listdir(txt_all_data_folder) if f.endswith('.txt')])

# ファイル名（拡張子を除く）が一致するか確認
assert len(image_files) == len(txt_files) and all([os.path.splitext(image)[0] == os.path.splitext(txt)[0] for image, txt in zip(image_files, txt_files)]), "画像とテキストのファイル名が一致しません。"

# ファイルをランダムにシャッフル
combined = list(zip(image_files, txt_files))
random.shuffle(combined)

# トレーニングセットとバリデーションセットに分割（8:2の比率）
split_index = int(len(combined) * 0.8)
train_files = combined[:split_index]
val_files = combined[split_index:]

# ファイルを対応するフォルダにコピー
def copy_files(files, source_folder_image, source_folder_txt, target_folder_image, target_folder_txt):
    cnt = 0
    for image_file, txt_file in files:
        print(cnt)
        shutil.copy(os.path.join(source_folder_image, image_file), target_folder_image)
        shutil.copy(os.path.join(source_folder_txt, txt_file), target_folder_txt)
        cnt = cnt+1

copy_files(train_files, image_all_data_folder, txt_all_data_folder, train_img_path, train_txt_path)
copy_files(val_files, image_all_data_folder, txt_all_data_folder, valid_img_path, valid_txt_path)

print("ファイルのコピーが完了しました。")
