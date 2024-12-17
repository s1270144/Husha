import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 画像ファイルのパス
image_paths = [
    '/home/iplslam/Husha/Data/Graph/cam1_onigajo_case01/frame_8293.jpg',
    '/home/iplslam/Husha/Data/Graph/cam2_onigajo_case01/frame_8293.jpg',
    '/home/iplslam/Husha/Data/Graph/cam3_onigajo_case01/frame_8293.jpg',
]

# 画像を読み込む
images = [mpimg.imread(img_path) for img_path in image_paths]

# 横並びで画像を表示
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, img, path in zip(axes, images, image_paths):
    ax.imshow(img)
    ax.axis('off')  # 軸を非表示にする
    # ファイル名を表示
    filename = path.split('/')[-1]  # ファイル名だけを取得
    ax.text(0.5, 1.05, filename, ha='center', va='bottom', fontsize=10, color='black', transform=ax.transAxes)

# 保存
output_path = '/home/iplslam/Husha/test1/onigajo_case01.jpg'  # 保存先のパス
plt.savefig(output_path, bbox_inches='tight', pad_inches=0)

# 終了
plt.close()
