import os

# ディレクトリパス
jpg_dir = '/home/iplslam/Husha/Dataset/1_3/all/jpg'
xml_dir = '/home/iplslam/Husha/Dataset/1_3/all/xml'
txt_dir = '/home/iplslam/Husha/Dataset/1_3/all/txt'

# ファイル名のセットを取得
jpg_files = set(os.path.splitext(f)[0] for f in os.listdir(jpg_dir) if f.endswith('.jpg'))
xml_files = set(os.path.splitext(f)[0] for f in os.listdir(xml_dir) if f.endswith('.xml'))
txt_files = set(os.path.splitext(f)[0] for f in os.listdir(txt_dir) if f.endswith('.txt'))

# print(jpg_files)
# print(xml_files)
# print(txt_files)

# 各ディレクトリにしか存在しないファイル名を特定
only_in_jpg = jpg_files - xml_files - txt_files
only_in_xml = xml_files - jpg_files - txt_files
only_in_txt = txt_files - jpg_files - xml_files

# 結果を表示
print("JPGディレクトリにのみ存在するファイル名:")
for filename in only_in_jpg:
    print(filename + '.jpg')

print("\nXMLディレクトリにのみ存在するファイル名:")
for filename in only_in_xml:
    print(filename + '.xml')

print("\nTXTディレクトリにのみ存在するファイル名:")
for filename in only_in_txt:
    print(filename + '.txt')
