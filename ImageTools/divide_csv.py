import pandas as pd
import os

# ベースディレクトリ（Tip.csvが存在するディレクトリ）
base_dir = "/home/iplslam/Husha/test/original/trimmed"

# Tip.csvのパス
tip_csv_path = os.path.join(base_dir, "Tip_3.csv")

# 各ディレクトリのパス
cam_dirs = {
    "cam1": os.path.join(base_dir, "cam1"),
    "cam2": os.path.join(base_dir, "cam2"),
    "cam3": os.path.join(base_dir, "cam3"),
}

# Tip.csvを読み込む
df = pd.read_csv(tip_csv_path)

# camカラムの値に基づいてフィルタリングして保存
for cam, cam_dir in cam_dirs.items():
    # 'cam'カラムに文字列cam1, cam2, cam3を含むレコードをフィルタリング
    filtered_df = df[df["cam"].str.contains(cam)]
    
    # 保存先のパスを作成
    output_path = os.path.join(cam_dir, f"{cam}.csv")
    
    # フィルタリングしたデータをCSVに保存
    filtered_df.to_csv(output_path, index=False)
    print(f"{output_path} に保存しました。")
