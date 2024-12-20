import os
import shutil

# Input
# input_dir = '/home/iplslam/Husha/Data/Yolo_images'
input_dir = '/home/iplslam/Husha/test/original'

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
            
            # 対応する画像ディレクトリ
            target_dir = os.path.join(camdir, source_image_dir)
            file_count = len([file for file in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, file))])
            if os.path.exists(target_dir):
                output_dir = os.path.join(output, f'{sub_dir}_{cam_dir}_jpg')
                copy_files(target_dir, output_dir, [f"{str(i).zfill(2)}.jpg" for i in range(0, file_count, 10)])

            # 対応するラベルディレクトリ
            target_dir = os.path.join(camdir, source_txt_dir)
            file_count = len([file for file in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, file))])
            if os.path.exists(target_dir):
                output_dir = os.path.join(output, f'{sub_dir}_{cam_dir}_txt')
                copy_files(target_dir, output_dir, [f"{str(i).zfill(2)}.txt" for i in range(0, file_count, 10)])

print("ファイルのコピーが完了しました。")
