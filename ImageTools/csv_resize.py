import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# 元のCSVファイルが格納されているルートディレクトリ
input_root_dir = '/home/iplslam/Husha/Data/tips/1'

# 処理されたCSVファイルを保存するルートディレクトリ
output_root_dir = '/home/iplslam/Husha/Data/tips/1_3'

def process_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        df = df // 3  # 全ての値を整数で1/2にする
        output_path = os.path.join(output_root_dir, os.path.basename(file_path))
        df.to_csv(output_path, index=False)
        print(f"{file_path} を処理しました。")
    except Exception as e:
        print(f"{file_path} の処理中にエラーが発生しました: {e}")

# スレッドプールを使用して並列処理する
with ThreadPoolExecutor(max_workers=8) as executor:
    file_paths = [os.path.join(input_root_dir, filename) for filename in os.listdir(input_root_dir) if filename.endswith('.csv')]
    futures = [executor.submit(process_csv, file_path) for file_path in file_paths]
    for future in futures:
        future.result()

print("すべてのCSVファイルが処理されました。")
