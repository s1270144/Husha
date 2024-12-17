import os
import shutil

# 元のディレクトリと新しいディレクトリのベースパス
base_dir = '/home/iplslam/Husha/Dataset/1_3/'
output_base_dir = '/home/iplslam/Husha/Dataset/1_3/all/'

# 拡張子ごとのディレクトリを作成
extensions = ['jpg', 'xml', 'txt']
for ext in extensions:
    ext_dir = os.path.join(output_base_dir, ext)
    if not os.path.exists(ext_dir):
        os.makedirs(ext_dir)

# 元のディレクトリ配下のディレクトリを走査
for parent_dir in os.listdir(base_dir):
    parent_path = os.path.join(base_dir, parent_dir)
            
    # ディレクトリのみ対象
    if os.path.isdir(parent_path):
        for filename in os.listdir(parent_path):
            file_path = os.path.join(parent_path, filename)
            
            # ファイルのみ対象
            if os.path.isfile(file_path):
                # ファイル名と拡張子を分離
                name, ext = os.path.splitext(filename)
                ext = ext.lstrip('.')
                
                # 拡張子に応じた出力ディレクトリを設定
                if ext in extensions:
                    output_dir = os.path.join(output_base_dir, ext)
                    
                    # 数字部分を抽出
                    number = name.split('_')[1]
                    # 新しいファイル名の作成
                    new_name = f"{parent_dir.split('_')[0]}_{number}.{ext}"
                    new_path = os.path.join(output_dir, new_name)

                    # ファイルをコピーしてリネーム
                    shutil.copy(file_path, new_path)

print("ファイルのリネームと移動が完了しました。")
