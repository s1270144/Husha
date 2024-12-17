import pandas as pd
import xml.etree.cElementTree as ET
import os

# CSVファイルと画像ディレクトリのパス
csv_file = '/home/iplslam/Husha/Data/tips/cam3.mp4.csv'
image_dir = '/home/iplslam/Husha/Data/images/cam3'  

# XMLファイルの保存先ディレクトリ
xml_output_dir = '/home/iplslam/Husha/Data/annotations/cam3'

# CSVファイルを読み込む
df = pd.read_csv(csv_file)

# 画像ファイル名のリストを取得
image_files = sorted(os.listdir(image_dir))

# XMLファイルを作成する関数
def create_xml_annotation(image_file, tip_x, tip_y, left, top, right, bottom):
    root = ET.Element("annotation")
    
    # ファイル名
    filename = ET.SubElement(root, "filename")
    filename.text = image_file
    
    # 画像のサイズ（仮の値）
    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    width.text = "960"  # 画像の幅
    height = ET.SubElement(size, "height")
    height.text = "540"  # 画像の高さ
    depth = ET.SubElement(size, "depth")
    depth.text = "3"  # 画像のチャンネル数
    
    # オブジェクト情報を追加
    object_elem = ET.SubElement(root, "object")
    name = ET.SubElement(object_elem, "name")
    name.text = "blade_tip"  # クラス名（例えば風車の羽の先端など）

    # 矩形の座標情報を追加
    bndbox = ET.SubElement(object_elem, "bndbox")
    xmin = ET.SubElement(bndbox, "xmin")
    xmin.text = left
    ymin = ET.SubElement(bndbox, "ymin")
    ymin.text = top
    xmax = ET.SubElement(bndbox, "xmax")
    xmax.text = right
    ymax = ET.SubElement(bndbox, "ymax")
    ymax.text = bottom
    
    # tip_xとtip_yを追加
    tip_x_elem = ET.SubElement(object_elem, "tip_x")
    tip_x_elem.text = tip_x
    tip_y_elem = ET.SubElement(object_elem, "tip_y")
    tip_y_elem.text = tip_y
    
    # XMLファイルを保存
    xml_filename = os.path.splitext(image_file)[0] + '.xml'
    xml_path = os.path.join(xml_output_dir, xml_filename)
    tree = ET.ElementTree(root)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)
    
    print(f"XMLファイル '{xml_filename}' を作成しました。")

# 各画像ごとにXMLファイルを作成
for idx, row in df.iterrows():
    tip_x = str(row['Tip_x'])
    tip_y = str(row['Tip_y'])
    left = str(row['Frame_left'])
    top = str(row['Frame_top'])
    right = str(row['Frame_right'])
    bottom = str(row['Frame_bottom'])
    
    image_file = image_files[idx]  # 画像ファイル名を取得
    create_xml_annotation(image_file, tip_x, tip_y, left, top, right, bottom)
