import os

# 実行
base_dir = "/home/iplslam/Husha/Dataset/Yolo_images"

def compare_and_clean_directories(base_dir):
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

    # ディレクトリペアを比較し、片方にしか存在しないファイルを削除
    for clean_name, dir_paths in directories.items():
        if len(dir_paths) == 2:  # _jpg と _txt が揃っている場合
            dir1, dir2 = dir_paths

            # 各ディレクトリ内のファイル一覧を取得（ファイル名のみ、拡張子は削除）
            files_dir1 = {os.path.splitext(file)[0] for file in os.listdir(dir1)}
            files_dir2 = {os.path.splitext(file)[0] for file in os.listdir(dir2)}

            # 差分ファイルを取得
            only_in_dir1 = files_dir1 - files_dir2
            only_in_dir2 = files_dir2 - files_dir1

            # 結果を表示
            print(f"'{clean_name}':")
            print(f"  {os.path.basename(dir1)} -> {len(files_dir1)} files")
            print(f"  {os.path.basename(dir2)} -> {len(files_dir2)} files")
            
            # 差分ファイルが存在する場合、削除を実行
            if only_in_dir1 or only_in_dir2:
                print("  -> ファイル数が一致していません！")
                if only_in_dir1:
                    print(f"    片方にしか存在しないファイル（削除対象: {os.path.basename(dir1)}）: {only_in_dir1}")
                    # 削除
                    for file in only_in_dir1:
                        file_path = os.path.join(dir1, f"{file}{os.path.splitext(os.listdir(dir1)[0])[1]}")
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            print(f"      削除: {file_path}")
                if only_in_dir2:
                    print(f"    片方にしか存在しないファイル（削除対象: {os.path.basename(dir2)}）: {only_in_dir2}")
                    # 削除
                    for file in only_in_dir2:
                        file_path = os.path.join(dir2, f"{file}{os.path.splitext(os.listdir(dir2)[0])[1]}")
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            print(f"      削除: {file_path}")
            else:
                print("  -> ファイル数は一致しています。")
        elif len(dir_paths) == 1:  # 片方のディレクトリしか存在しない場合
            print(f"'{clean_name}' は片方のディレクトリしか存在しません: {dir_paths[0]}")

compare_and_clean_directories(base_dir)