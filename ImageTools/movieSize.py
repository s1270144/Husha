import cv2

# 入力動画ファイルと出力動画ファイルのパス
input_video_path = '../Data/movie/1/cam1.mp4'
output_video_path = '../Data/movie/1_2/cam1.mp4'

# 動画キャプチャを開く
cap = cv2.VideoCapture(input_video_path)

# 入力動画のプロパティを取得
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 出力動画のプロパティを設定
new_width = width // 2
new_height = height // 2

# ビデオライターを作成
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (new_width, new_height))

# フレームごとに動画を読み込み、リサイズして出力
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # フレームをリサイズ
    resized_frame = cv2.resize(frame, (new_width, new_height))
    # リサイズされたフレームを書き込む
    out.write(resized_frame)

# リソースを解放
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"動画のサイズ変更が完了しました: {output_video_path}")
