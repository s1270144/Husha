import pandas as pd

# CSVファイルのパス
input_path = '/home/iplslam/Husha/test.csv'
output_path = '/home/iplslam/Husha/origin.csv'

# CSVファイルをデータフレームとして読み込む
df = pd.read_csv(input_path)

# 新しいカラムを作成
df['Frame_ID'] = df.index
df.rename(columns={
    'Frame_left': 'xmin',
    'Frame_top': 'ymin',
    'Frame_right': 'xmax',
    'Frame_bottom': 'ymax'
}, inplace=True)

# 必要なカラムの順序でデータフレームを再構成
df = df[['Frame_ID', 'Tip_x', 'Tip_y', 'xmin', 'ymin', 'xmax', 'ymax']]

# 新しいCSVファイルに保存
df.to_csv(output_path, index=False)

print(f'Converted CSV file saved to {output_path}')
