import pandas as pd

# fps.csv を読み込む
df = pd.read_csv('/home/iplslam/Husha/test/original/trimmed/fps_original.csv')

# FPS を計算 (fps = 1 / cam_time)
df['fps'] = 1 / df['cam_fps']

# FPS の平均値を計算
fps_mean = df['fps'].mean()

# 結果を表示
print(f"FPS の平均値: {fps_mean:.2f}")
