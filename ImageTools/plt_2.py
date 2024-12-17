import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルのパス
fasterrcnn_path = '/home/iplslam/Husha/createDataset/fasterrcnn_predictions.csv'
yolo_path = '/home/iplslam/Husha/createDataset/yolo_predictions.csv'

# CSVファイルをデータフレームとして読み込む
fasterrcnn_df = pd.read_csv(fasterrcnn_path)
yolo_df = pd.read_csv(yolo_path)

# Score列を0.1区切りでビンに分けてカウントする
bins = [i / 10 for i in range(11)]  # 0.0, 0.1, ..., 1.0
fasterrcnn_counts = pd.cut(fasterrcnn_df['Score'], bins=bins).value_counts().sort_index()
yolo_counts = pd.cut(yolo_df['Score'], bins=bins).value_counts().sort_index()

# データフレームに変換
df = pd.DataFrame({
    'Score': fasterrcnn_counts.index.astype(str),
    'Faster R-CNN': fasterrcnn_counts.values,
    'YOLO': yolo_counts.values
})

# プロットの作成
df.set_index('Score').plot(kind='bar', stacked=True, color=['blue', 'red'], figsize=(12, 6))

# グラフのラベルとタイトルを設定
plt.xlabel('Score Range')
plt.ylabel('Count')
plt.title('Score Distribution for Faster R-CNN and YOLO')
plt.legend(title='Model')
plt.grid(True)

# グラフを表示
plt.show()
