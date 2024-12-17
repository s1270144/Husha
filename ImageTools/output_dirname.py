import os

# ベースとなるディレクトリパス
base_dir = '/home/iplslam/Husha/Data/Graph'

# サブディレクトリ名を格納するリスト
subdirectories = []

# ベースディレクトリ内の各項目を確認
for item in os.listdir(base_dir):
    item_path = os.path.join(base_dir, item)
    # サブディレクトリのみを対象
    if os.path.isdir(item_path):
        subdirectories.append(item)

# サブディレクトリ名をソート
subdirectories.sort()

# ソートされたサブディレクトリ名を出力
print("サブディレクトリ名 (ソート済み):")
for subdir in subdirectories:
    print(subdir)
