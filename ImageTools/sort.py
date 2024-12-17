import os
import shutil

# 基本ディレクトリ
base_dir = '/home/iplslam/Husha/Dataset/Yolo_images'

# 出力ディレクトリを作成
output_txt_dir = os.path.join(base_dir, 'txt')
output_jpg_dir = os.path.join(base_dir, 'jpg')
os.makedirs(output_txt_dir, exist_ok=True)
os.makedirs(output_jpg_dir, exist_ok=True)

# サブディレクトリからファイルを収集
txt_files = []
jpg_files = []

for subdir in os.listdir(base_dir):
    subdir_path = os.path.join(base_dir, subdir)
    if os.path.isdir(subdir_path):
        # .txtファイルを収集
        txt_files.extend([os.path.join(subdir_path, f) for f in os.listdir(subdir_path) if f.endswith('.txt')])
        # .jpgファイルを収集
        jpg_files.extend([os.path.join(subdir_path, f) for f in os.listdir(subdir_path) if f.endswith('.jpg')])

# ファイルをソートして順番にリネーム＆移動
for i, txt_file in enumerate(sorted(txt_files)):
    new_txt_name = f"frame_{i}.txt"
    shutil.move(txt_file, os.path.join(output_txt_dir, new_txt_name))

for i, jpg_file in enumerate(sorted(jpg_files)):
    new_jpg_name = f"frame_{i}.jpg"
    shutil.move(jpg_file, os.path.join(output_jpg_dir, new_jpg_name))

print(f"TXT files have been moved to: {output_txt_dir}")
print(f"JPG files have been moved to: {output_jpg_dir}")
