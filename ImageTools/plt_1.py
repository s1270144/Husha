import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルのパス
fasterrcnn_path = '/home/iplslam/Husha/createDataset/fasterrcnn_predictions.csv'
yolo_path = '/home/iplslam/Husha/createDataset/yolo_predictions.csv'

# CSVファイルをデータフレームとして読み込む
fasterrcnn_df = pd.read_csv(fasterrcnn_path)
yolo_df = pd.read_csv(yolo_path)

# Frame_IDとScoreの列を抽出
fasterrcnn_scores = fasterrcnn_df[['Frame_ID', 'Score']]
yolo_scores = yolo_df[['Frame_ID', 'Score']]

# Frame_IDでソート
fasterrcnn_scores = fasterrcnn_scores.sort_values(by='Frame_ID')
yolo_scores = yolo_scores.sort_values(by='Frame_ID')

# プロットの作成
plt.figure(figsize=(12, 6))
plt.plot(fasterrcnn_scores['Frame_ID'], fasterrcnn_scores['Score'], label='Faster R-CNN', color='blue')
plt.plot(yolo_scores['Frame_ID'], yolo_scores['Score'], label='YOLO', color='red')

# グラフのラベルとタイトルを設定
plt.xlabel('Frame_ID')
plt.ylabel('Score')
plt.title('Frame_ID vs Score')
plt.legend()
plt.grid(True)

# グラフを表示
plt.show()
