# ImageTools ディレクトリ詳細

- calc_csv.py: &ensp;csvの”Processing_Time”の平均値を算出

- **check.py: &ensp;作成されたフレーム座標と先端座標が正しく取得できているかの確認**

- clipcut.py: &ensp;画像の特定の範囲を切り取って保存（資料作成用）

- **create_dataset.py: &ensp;pklファイルの作成**

- **createTxt.py: &ensp;指定ディレクトリ内の画像のフレーム座標を正規化してtxtファイルを作成**

- csv_resize.py : &ensp;csvファイルの情報（画像サイズ、座標など）をリサイズ

- csv_test.py: &ensp;必要なカラムの順序でデータフレームを再構成

- **csvToXml_v1.py: &ensp;指定ディレクトリ内の各画像ごとにxmlファイルを作成(一つのcsv)**

- **csvToXml_v2.py: &ensp;v1の汎用性高いコード。ディレクトリ内の複数のcsvから一括でxmlを作成できる**

- **duplicate.py: &ensp;特定ファイルの複製。**
<!-- 学習時間を短縮するため、50フレームごとの画像とそれに対応するxml, txtファイルを複製 -->

- filename_check.py:&ensp;各ディレクトリにしか存在しないファイル名を特定
<!-- 学習の際のエラーを防止するため -->

- **ioa.py: &ensp;IoAを計算**

- mergeFile.py: &ensp;画像整理。今は使用していない。

- movie_cut.py: &ensp;動画の開始位置、終了位置を指定して、範囲内の動画を保存

- movieSize.py: &ensp;動画のフレームサイズの変更

- plt_bar.py: &ensp;FPSの比較

- resize.py: &ensp;ディレクトリ内の画像をすべて縮小して新たなディレクトリに保存する

- splitData_txt.py: &ensp;学習データと評価データを 8 : 2 に分割（txt）

- splitData_xml.py: &ensp;学習データと評価データを 8 : 2 に分割（xml）

<!-- 学習データと評価データは分割しない。評価データは別動画のデータを使用する -->

## yoloの学習データ作成フロー
1. check_tip_offset.py: &ensp;test_original.pyで取得した先端座標が正しいデータなのか描写して確認＆座標データを(1920, 1080)用座標からクリップ画像用座標に変換してcsvファイルを作成する
2. createTxt.py: &ensp;csvファイル＆対応画像の情報をもとにYolo用のtxtファイルを作成する
3. dupulicate.py: &ensp;学習に使用する分の画像尾を指定するディレクトリに複製
4. sort.py &ensp;

jpgディレクトリとtxtファイルのディレクトリが一致しない場合、fileNumCheck.pyを使用すると良い。