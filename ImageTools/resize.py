import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# 元の画像ファイルが格納されているルートディレクトリ
input_root_dir = 'Data/images/1'

# 縮小された画像ファイルを保存するルートディレクトリ
output_root_dir = 'Data/images/1_3'

def resize_image(file_path, output_dir):
    try:
        img = Image.open(file_path)
        img_resized = img.resize((img.width // 3, img.height // 3))
        output_path = os.path.join(output_dir, os.path.basename(file_path))
        img_resized.save(output_path)
        print(f"{file_path} を処理しました。")
    except Exception as e:
        print(f"{file_path} の処理中にエラーが発生しました: {e}")

def process_directory(directory):
    input_dir = os.path.join(input_root_dir, directory)
    output_dir = os.path.join(output_root_dir, directory)

    os.makedirs(output_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=8) as executor:
        file_paths = [os.path.join(input_dir, filename) for filename in os.listdir(input_dir) if filename.endswith('.jpg')]
        futures = [executor.submit(resize_image, file_path, output_dir) for file_path in file_paths]
        for future in futures:
            future.result()

# ルートディレクトリ内のすべてのサブディレクトリを処理する
for directory in os.listdir(input_root_dir):
    dir_path = os.path.join(input_root_dir, directory)
    if os.path.isdir(dir_path):
        process_directory(directory)

print("すべての画像ファイルが縮小されました。")
