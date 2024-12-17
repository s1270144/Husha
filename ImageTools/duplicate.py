import os
import shutil

# Input
input_dir = '/home/iplslam/Husha/Data/Yolo_images'

# Output
output = '/home/iplslam/Husha/Dataset/Yolo_images'

source_image_dir = 'blade_images'
source_txt_dir = 'processed_points'
target_csv = 'processed_points.csv'

# ファイルを検索してコピーする関数
def copy_files(source_dir, target_dir, extensions):
    os.makedirs(target_dir, exist_ok=True)
    for file in os.listdir(source_dir):
        if any(ext in file for ext in extensions):
            source_file_path = os.path.join(source_dir, file)
            target_file_path = os.path.join(target_dir, file)
            shutil.copy(source_file_path, target_file_path)
            print(f"Copied {file} to {target_file_path}")

# アノテーションの各ディレクトリを処理
for sub_dir in os.listdir(input_dir):
    subdir = os.path.join(input_dir, sub_dir)
    # print('DirName ' + subdir)

    for cam_dir in os.listdir(subdir):
        if 'cam' in cam_dir: 
            camdir = os.path.join(subdir, cam_dir)
            # print('---' + camdir)
        else: continue

        for target_dir in os.listdir(camdir):
            target_dir = os.path.join(camdir, source_image_dir)
            # 対応する画像ディレクトリ
            if os.path.exists(target_dir):
                output_dir = os.path.join(output, f'{sub_dir}_{cam_dir}_jpg')
                copy_files(target_dir, output_dir, ["50.jpg", "00.jpg"])

            target_dir = os.path.join(camdir, source_txt_dir)
            # 対応する画像ディレクトリ
            if os.path.exists(target_dir):
                output_dir = os.path.join(output, f'{sub_dir}_{cam_dir}_txt')
                copy_files(target_dir, output_dir, ["50.txt", "00.txt"])

print("ファイルのコピーが完了しました。")
