import os
import pickle
import xml.etree.ElementTree as ET
from PIL import Image

# パス設定
data_dir = '/home/iplslam/Husha/Dataset/1_3'
dataset_path = '/home/iplslam/Husha/Dataset/jpg_xml_1_3/wind_turbine_dataset_1_3.pkl'

# アノテーション読み込み
def read_annotations(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        boxes = []
        labels = []
        for obj in root.findall('object'):
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)

            # バウンディングボックスの検証
            if xmin >= xmax or ymin >= ymax or xmin < 0 or ymin < 0:
                raise ValueError(f"Invalid bounding box in {xml_path}")

            boxes.append([xmin, ymin, xmax, ymax])
            labels.append(1)  # Assuming label 1 for the wind turbine blades

        return boxes, labels

    except Exception as e:
        print(f"Error processing {xml_path}: {e}")
        return [], []

# すべての画像およびアノテーションファイルを収集する
image_files = []
annotation_files = []
for subdir in os.listdir(data_dir):
    if subdir.endswith('_jpg'):
        annotation_subdir = subdir.replace('_jpg', '_xml')
        image_subdir_path = os.path.join(data_dir, subdir)
        annotation_subdir_path = os.path.join(data_dir, annotation_subdir)
        if os.path.exists(annotation_subdir_path):
            for img_file in sorted(os.listdir(image_subdir_path)):
                if img_file.endswith('.jpg'):
                    img_path = os.path.join(image_subdir_path, img_file)
                    xml_file = img_file.replace('.jpg', '.xml')
                    xml_path = os.path.join(annotation_subdir_path, xml_file)
                    if os.path.exists(xml_path):
                        image_files.append(img_path)
                        annotation_files.append(xml_path)

# データセットオブジェクトを保存する
with open(dataset_path, 'wb') as f:
    pickle.dump((image_files, annotation_files), f)

print("Dataset creation completed and saved.")

# データセットオブジェクトの確認
print("Verifying the saved dataset...")
with open(dataset_path, 'rb') as f:
    image_files, annotation_files = pickle.load(f)

# 先頭の数件を表示して確認
num_samples_to_check = 5
print(f"Total samples: {len(image_files)}")
for i in range(min(num_samples_to_check, len(image_files))):
    print(f"Sample {i+1}:")
    print(f"Image file: {image_files[i]}")
    print(f"Annotation file: {annotation_files[i]}")
    boxes, labels = read_annotations(annotation_files[i])
    print(f"Bounding boxes: {boxes}")
    print(f"Labels: {labels}")

print("Dataset verification completed.")