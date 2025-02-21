## ディレクトリ構成
- Data: 動画やアノテーションファイルなど
- Dataset: 学習に使用するデータセット格納（最重要）
- FasterRCNN: Faster R-CNN
- test1: 本システム(test3.py)実行時に必要
- ImageTools: データセット作成や整理する画像処理のコードを格納
- results: テストで作成された画像やcsvファイル等
- yolov5: Yolov5

## メインファイル
- test_original.py
    - Template Matchingでブレード捕捉、GrabCutでブレードの領域抽出を行う
    - BladeCapture.pyをimportしている
- test_yolo.py
    - Yoloでブレード捕捉、Yoloで先端捕捉を行う
    - BladeCapture_yolo.pyをimportしている

## 命名規則
- __1__ : オリジナルサイズ（1920 x 1080）
- __1_2__ : 1/2サイズ（960 x 540）
- __1_3__ : 1/3サイズ（640 x 360）

## DataSet
- csvファイル: txtやxmlの作成や結果のプロットの作成に必要
- txtファイル: Yoloの学習に必要（画像とcsvから作成）
- xmlファイル: Faster R-CNN の学習に必要（アノテーションファイル）

## test_original.pyの実行（BladeCapture.pyをimport）
1. python3 test3.py
2. ドラックして対象領域を囲む
3. コマンド入力（詳細はBladeCapture1.py）してガイド
4. ｎで実行
5. Escで実行

## Yolo実行
学習（ブレード）: python3 train.py --data data/BladeFrame.yaml --weight yolov5s.pt --epochs 5
学習（先端）: python3 train.py --data data/BladeTip.yaml --weight yolov5s.pt --epochs 5

検出: python3 detect.py --source /home/iplslam/Husha/Data/onigajo/20230208/case01/cam1.mp4 --weights /home/iplslam/Husha/yolov5/runs/train/1/weights/best.pt

## 更新
2025/3

GitHub https://github.com/s1270144/Husha