## Blender のそれぞれの UI アイコンを画像ファイル(png)として取得する

* [Blender Developer Talk](https://devtalk.blender.org/t/new-icons-for-blender-2-8x/4651)にあるように、Blender の UI のアイコン画像(svg)は [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)のもとで提供されている
	> This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.<br>
	> Icons within Blender must be used only for functions they were designed for in order to maintain GUI’s internal integrity, to keep good UX under control and to avoid confusion.

* 以下のアイコン画像(png)はこの svg ファイルから作成されており、同様に[Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)のもとで提供する


### アイコンをまとめたzip  (透過png形式)：　[20×20 のアイコン](https://github.com/nikogoli/Blender_UI_icons_png/blob/main/png_icons(20_20).zip)、　[40×40 のアイコン](https://github.com/nikogoli/Blender_UI_icons_png/blob/main/png_icons(40_40).zip)<br>
※ スカルプトのブラシやキーフレームなど、含まれていないものもある<br>
※ 透過 + 白線 なので、白背景ではほぼ見えない<br>
※ 見落としでなければ、2.90 において未使用のアイコンが7個、重複するアイコンが2つ含まれる　

---------------------------------------------------------

* 元となるアイコン画像：[ここ](https://developer.blender.org/diffusion/B/browse/master/release/datafiles)の「blender_icons.svg」<br>
	※ 上の Developer Talk のファイルから少し変更されている
* svgファイルの形式：30行×26列、各マスにアイコンが設置されている<br>
	(枠線あり、空白マスあり、Blender内部のアイコン名の順序とは部分的にのみ一致する)

Inkscape などで svg を直接扱える人は、このファイルをいい感じに処理すればよい(はず)
<br><br>


### Inkscape を扱えず、Illustrator も持っていない人は・・・
------------------------------
1. Gimp を入手する
1. Gimp を起動して svg ファイルをドロップするか、「レイヤーとして開く」から読み込む<br>
	※「パスのインポート」を使うと(大量の)パスとして読み込めるが、gimp 2.10.14 ではいくつかのアイコンで位置ズレが生じていたので推奨はしない
1. 読み込みにおいて、希望に合うサイズを選ぶ<br>
	※ 等倍の場合、アイコンのサイズは 20×20 になり、かなり小さめ
1. 左右と下部のインデックスを消去したうえで、png などでエクスポートする<br>
	※ 一部のインデックスはアイコンのマスに重なっているので邪魔になる
1. 画像を、各々の得意な方法で分割する
1. 分割された画像のうち、空白マスの画像を消去する
1. [`names.txt`](https://github.com/nikogoli/Blender_UI_icons_png/blob/main/names.txt)の中身をリストして読み込み、残りの画像の対して作成された順に適用する<br>
	※ `names.txt`の中身は、「1行目の1列目のアイコン名 \n 2列目のアイコン名 \n 3列目 \n ・・・\n 2行目の1列目 \n 2列目 \n 3列目\n ・・・」となっている
1. それぞれの画像を保存して終わり
<br><br>

### 画像の分割方法の考え方の例　(等倍の svg の場合)
--------------------------
* アイコンのサイズは 20×20 で、サイズ1の枠線に囲まれている
* 作業の流れ
	1. 必要な部分をトリミング
	2. 枠も含めた 21×21 のブロックに分割
	1. 各ブロックを 20×20 にトリミングし、枠を消去

#### 「必要な部分」とは？
* 等倍で読み込んだ svg から 作成した png ファイルのサイズ： 602(横)×640(縦)
* 21×21 のブロックが 30行×26列 あるときのサイズ： 546(横)×630(縦)
* png ファイルの上部において、8行のピクセルはインデックス部分なので不要
* png ファイルの左側において、3列のピクセルはインデックス部分なので不要

　　　　　　　↓<br>
 画像のうち必要な部分は、「左上から元のピクセルの 9～638 行と 4～549 列」の部分<br>
 ※ svg を2倍にした場合は、同様に考えて「18～1278 行と 8～1098 列」の部分
 <br><br>


<details><summary>使ったコード (python)</summary>
  
```python
from pathlib import Path
import warnings

import numpy as np
import skimage.io
import skimage.util

# 画像保存のスキップ判断に skimage.io.imsave()の warngin を使うために、警告を例外として扱う
warnings.resetwarnings()
warnings.simplefilter('error') 

home = Path("==working directory path==")
source_path = Path(home, "==source file name==")
out_path = Path(home, "==output directory name==")

names_text = Path(home, "names.txt")
with names_text.open("r", encoding="utf-8") as fr:
    names = [x.rstrip() for x in fr.readlines()]  #names.txt の中身は "NAME1\nNAME2\n..."

img = skimage.io.imread(str(source_path))
blocks_copy = skimage.util.view_as_blocks(img[8:638, 3:549, :], (21, 21, 4)).copy()
# svg を2倍にして分割対象のファイルを作った場合は↓のようにする
#blocks_copy = skimage.util.view_as_blocks(img[16:1276, 6:1098, :], (42, 42, 4)).copy()


idx = 0
for row_id in range(30):  # 列数・行数は blocks_copy.shape で取得できる
    for col_id in range(26):
        name = names[idx]
        file_path = Path(out_path, f"{name}.png")
	# 画像に枠しかない場合、io.imsave()が low contrast warning を出すので、
	# この警告を例外としてキャッチし、空白マスの画像の保存をスキップする
        try:
            skimage.io.imsave(str(file_path), blocks_copy[row_id, col_id, 0][0:20, 0:20]) #トリミングして保存
            idx += 1
        except UserWarning:
            pass
	# names.txt は「空白マスなし」状態を基準にしているので、名前のズレとIndexError を避けるため空白マスの保存のスキップが必要
	# なので、names.txt を作り直せばこのあたりの処理は不要
```
</details>


