from PIL import Image

def crop_image(input_image_path, output_image_path, crop_area):
    """
    画像の特定の範囲を切り取って保存する。

    :param input_image_path: 入力画像のファイルパス
    :param output_image_path: 出力画像のファイルパス
    :param crop_area: 切り取る範囲（x1, y1, x2, y2）
    """
    # 画像を開く
    image = Image.open(input_image_path)

    # 画像を切り取る
    cropped_image = image.crop(crop_area)

    # 切り取った画像を保存する
    cropped_image.save(output_image_path)

# 入力画像と出力画像のパスを指定
input_image_path = '/home/iplslam/Husha/yolov5/runs/detect/1/frame_670.jpg'
output_image_path = 'yolo_670.jpg'

# 切り取る範囲を指定（左上の(x1, y1)から右下の(x2, y2)）
crop_area = (600, 150, 1500, 750)

# 画像を切り取って保存
crop_image(input_image_path, output_image_path, crop_area)
