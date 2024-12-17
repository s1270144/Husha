import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルパス
file_paths = [
    "/home/iplslam/Husha/test/original/case01/throughput_original.csv",
    "/home/iplslam/Husha/test/yolo/case01/throughput_yolo.csv"
]

# 各ファイルの平均FPSを格納する辞書
avg_fps = {}

# 各CSVファイルのFPSを計算
for file_path in file_paths:
    # CSVファイルを読み込む
    df = pd.read_csv(file_path)
    
    # cam_fps列が存在するか確認
    if 'throughput' in df.columns:
        # FPSを計算（1 / cam_fps）
        df['fps'] = 1 / df['throughput']
        
        # 平均FPSを計算して格納
        avg_fps[file_path.split('/')[-1]] = df['fps'].mean()
    else:
        print(f"'cam_fps'カラムが見つかりません: {file_path}")

# グラフ設定
fig, ax = plt.subplots(figsize=(6, 4))  # 画像のサイズを指定
bar_width = 0.3  # 棒の太さを指定

# 横棒グラフを作成
ax.barh(list(avg_fps.keys()), list(avg_fps.values()), color='skyblue', height=bar_width)

# ラベルとタイトルの設定
ax.set_xlabel('Average FPS', fontsize=10)
ax.set_title('Average FPS for Each File', fontsize=12)
plt.tight_layout()

# グラフの保存
output_path = "/home/iplslam/Husha/test/compare/average_fps_plot_case01.png"
plt.savefig(output_path, dpi=300)  # 解像度を指定して保存
print(f"グラフを保存しました: {output_path}")
