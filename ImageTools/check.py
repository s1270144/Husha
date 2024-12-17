import cv2
import pandas as pd
import os

def main(video_path, csv_path, output_dir):
    # 動画を読み込み
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("動画を開けませんでした")
        return

    # CSVファイルを読み込み
    df = pd.read_csv(csv_path)
    csv_index = 0
    total_rows = len(df)

    # フレームサイズを指定
    frame_width = 1920
    frame_height = 1080

    # 表示ウィンドウサイズを指定
    display_width = 640
    display_height = 360

    frame_cnt = 0

    # ウィンドウを作成
    cv2.namedWindow('Video')

    # 最初に10フレーム進める
    for _ in range(10):
        ret, frame = cap.read()
        if not ret:
            print("動画の読み込みが終了しました")
            return

    while cap.isOpened():
        if csv_index < total_rows:
            # 現在の行のデータを取得
            row = df.iloc[csv_index]
            tip_x, tip_y = int(row['Tip_x']), int(row['Tip_y'])
            frame_left, frame_top, frame_right, frame_bottom = int(row['Frame_left']), int(row['Frame_top']), int(row['Frame_right']), int(row['Frame_bottom'])

            # フレームをリサイズ
            frame = cv2.resize(frame, (frame_width, frame_height))

            # 学習データ作成
            frame_filename = os.path.join(output_dir, f"frame_{frame_cnt}.jpg")
            frame_cnt += 1

            # 赤い点をプロット
            cv2.circle(frame, (tip_x, tip_y), 5, (0, 0, 255), -1)

            # 青い矩形をプロット
            cv2.rectangle(frame, (frame_left, frame_top), (frame_right, frame_bottom), (255, 0, 0), 2)
        
            # CSVファイルの次の行を表示
            csv_index += 1
        
        # フレームを表示ウィンドウサイズにリサイズして表示
        display_frame = cv2.resize(frame, (display_width, display_height))
        # cv2.imwrite(frame_filename, frame)
        cv2.imshow('Video', display_frame)

        # 動画を1フレーム進める
        ret, frame = cap.read()
        if not ret:
            print("動画の読み込みが終了しました")
            break

        # もしqを押す場合、処理を中断する
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# 使用例
video_path = '/home/iplslam/Husha/Data/movie/1/cam3.mp4'
csv_path = '/home/iplslam/Husha/Data/tips/1/cam3.mp4.csv'
output_dir = "/home/iplslam/Husha/results/test_3"
main(video_path, csv_path, output_dir)
