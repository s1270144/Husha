import os

# ベースディレクトリ
base_dir = "/home/iplslam/Husha/Dataset/Yolo_images"

# キーワード
keywords = ["_jpg", "_txt"]

# キーワードを取り除いたディレクトリをキーとし、対応するパスを格納する辞書
directories = {}

# ディレクトリを走査
for dirname in os.listdir(base_dir):
    dir_path = os.path.join(base_dir, dirname)
    if os.path.isdir(dir_path):  # ディレクトリのみ処理
        # キーワードを取り除いた名前を生成
        clean_name = dirname
        for keyword in keywords:
            clean_name = clean_name.replace(keyword, "")
        # 同じ名前のディレクトリをまとめる
        if clean_name not in directories:
            directories[clean_name] = []
        directories[clean_name].append(dir_path)

# ファイル数を比較
for clean_name, dir_paths in directories.items():
    if len(dir_paths) == 2:  # _jpg と _txt が揃っている場合
        dir1, dir2 = dir_paths
        # 各ディレクトリ内のファイル数を取得
        num_files_dir1 = len(os.listdir(dir1))
        num_files_dir2 = len(os.listdir(dir2))
        
        # 結果を表示
        print(f"'{clean_name}':")
        print(f"  {os.path.basename(dir1)} -> {num_files_dir1} files")
        print(f"  {os.path.basename(dir2)} -> {num_files_dir2} files")
        if num_files_dir1 == num_files_dir2:
            print("  -> ファイル数は一致しています。")
        else:
            print("  -> ファイル数が一致していません！")
    elif len(dir_paths) == 1:  # 片方のディレクトリしか存在しない場合
        print(f"'{clean_name}' は片方のディレクトリしか存在しません: {dir_paths[0]}")
