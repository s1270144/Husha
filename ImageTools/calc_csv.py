import pandas as pd

# CSVファイルのパス
csv_file_path = '/home/iplslam/Husha/FasterRCNN/results/1_3/output/frame_processing_times.csv'

# CSVファイルを読み込む
df = pd.read_csv(csv_file_path)

# 0~99行目のProcessing_Timeの平均値を計算
average_processing_time = df.loc[0:99, 'Processing_Time'].mean()

print(f'0〜99行目のProcessing_Timeの平均値: {average_processing_time:.6f}秒')
print(f'FPS: {1/average_processing_time}')
