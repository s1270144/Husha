import pandas as pd
import numpy as np

# CSVファイルのパス
origin_path = '/home/iplslam/Husha/origin.csv'
fasterrcnn_path = '/home/iplslam/Husha/createDataset/fasterrcnn_predictions.csv'
yolo_path = '/home/iplslam/Husha/createDataset/yolo_predictions.csv'

# データの読み込み
origin = pd.read_csv(origin_path)
fasterrcnn_predictions = pd.read_csv(fasterrcnn_path)
yolo_predictions = pd.read_csv(yolo_path)

# バウンディングボックスの面積を計算する関数
def bbox_area(bbox):
    return (bbox['xmax'] - bbox['xmin']) * (bbox['ymax'] - bbox['ymin'])

# バウンディングボックスのIoAを計算する関数
def calculate_ioa(true_bbox, pred_bbox):
    # 重なり部分の座標
    x_left = max(true_bbox['xmin'], pred_bbox['xmin'])
    y_top = max(true_bbox['ymin'], pred_bbox['ymin'])
    x_right = min(true_bbox['xmax'], pred_bbox['xmax'])
    y_bottom = min(true_bbox['ymax'], pred_bbox['ymax'])

    # 重なり部分の面積
    if x_right > x_left and y_bottom > y_top:
        inter_area = (x_right - x_left) * (y_bottom - y_top)
    else:
        inter_area = 0

    # 予測バウンディングボックスの面積
    pred_area = bbox_area(pred_bbox)

    # IoAの計算
    if pred_area > 0:
        ioa = inter_area / pred_area
    else:
        ioa = 0

    return ioa

# IoAの計算
def compute_ioa(predictions, origin_boxes):
    ioa_results = []
    for _, true_row in origin_boxes.iterrows():
        true_bbox = {
            'xmin': true_row['xmin'],
            'ymin': true_row['ymin'],
            'xmax': true_row['xmax'],
            'ymax': true_row['ymax']
        }
        frame_id = true_row['Frame_ID']
        
        # 対応する予測バウンディングボックスを取得
        pred_boxes = predictions[predictions['Frame_ID'] == frame_id]
        
        # 各予測バウンディングボックスに対してIoAを計算
        for _, pred_row in pred_boxes.iterrows():
            pred_bbox = {
                'xmin': pred_row['xmin'],
                'ymin': pred_row['ymin'],
                'xmax': pred_row['xmax'],
                'ymax': pred_row['ymax']
            }
            ioa = calculate_ioa(true_bbox, pred_bbox)
            ioa_results.append({
                'Frame_ID': frame_id,
                'Tip_x': true_row['Tip_x'],
                'Tip_y': true_row['Tip_y'],
                'xmin': pred_bbox['xmin'],
                'ymin': pred_bbox['ymin'],
                'xmax': pred_bbox['xmax'],
                'ymax': pred_bbox['ymax'],
                'IoA': ioa,
                'Score': pred_row.get('Score', np.nan),  # Scoreが存在しない場合はNaN
                'Processing_Time': pred_row.get('Processing_Time', np.nan)  # Processing_Timeが存在しない場合はNaN
            })
    
    return pd.DataFrame(ioa_results)

# IoAを計算
fasterrcnn_ioas = compute_ioa(fasterrcnn_predictions, origin)
yolo_ioas = compute_ioa(yolo_predictions, origin)

# IoAの平均値と中央値を計算
fasterrcnn_mean_ioa = fasterrcnn_ioas['IoA'].mean()
fasterrcnn_median_ioa = fasterrcnn_ioas['IoA'].median()
yolo_mean_ioa = yolo_ioas['IoA'].mean()
yolo_median_ioa = yolo_ioas['IoA'].median()

# 結果をCSVファイルに保存
fasterrcnn_ioas.to_csv('/home/iplslam/Husha/fasterrcnn_ioa.csv', index=False)
yolo_ioas.to_csv('/home/iplslam/Husha/yolo_ioa.csv', index=False)

# 結果の表示
print(f'Faster R-CNN IoA results saved to /home/iplslam/Husha/fasterrcnn_ioa.csv')
print(f'YOLO IoA results saved to /home/iplslam/Husha/yolo_ioa.csv')
print(f'Faster R-CNN Mean IoA: {fasterrcnn_mean_ioa:.4f}')
print(f'Faster R-CNN Median IoA: {fasterrcnn_median_ioa:.4f}')
print(f'YOLO Mean IoA: {yolo_mean_ioa:.4f}')
print(f'YOLO Median IoA: {yolo_median_ioa:.4f}')
