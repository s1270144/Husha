import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルパス
file_paths = [
    "/home/iplslam/Husha/test/original/case02_1/throughput_original.csv",
    "/home/iplslam/Husha/test/yolo/case02_1/throughput_yolo.csv",
]

# 各ファイルの平均FPSを格納する辞書
avg_tp = {}

# 各CSVファイルのFPSを計算
for file_path in file_paths:
    # CSVファイルを読み込む
    df = pd.read_csv(file_path)
    
    # throughput列が存在するか確認
    if 'throughput' in df.columns:
        # FPSを計算（1 / cam_fps）
        df['tp'] = 1 / df['throughput']
        
        # 平均throughputを計算して格納
        avg_tp[file_path.split('/')[-1]] = df['tp'].mean()
    else:
        print(f"'throughput'カラムが見つかりません: {file_path}")

# グラフ設定
fig, ax = plt.subplots(figsize=(6, 4))  # 画像のサイズを指定
bar_width = 0.3  # 棒の太さを指定

# 横棒グラフを作成
ax.barh(['Existing\nImage Processing\nPipeline', 'YOLO'], list(avg_tp.values()), color='skyblue', height=bar_width)

# ラベルとタイトルの設定
ax.set_xlabel('Average Throughput', fontsize=10)
ax.set_title('Average Throughput', fontsize=12)
plt.tight_layout()

# グラフの保存
output_path = "/home/iplslam/Husha/test/compare/avg_tp_case02_1.png"
plt.savefig(output_path, dpi=300)  # 解像度を指定して保存
print(f"グラフを保存しました: {output_path}")
