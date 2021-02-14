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
            skimage.io.imsave(str(file_path), blocks_copy[row_id, col_id, 0][0:20, 0:20]) #トリミング
            idx += 1
        except UserWarning:
            pass
            # names.txt は「空白マスなし」状態を基準にしているので、名前のズレと IndexError を避けるために空白マスのスキップが必要
            # なので、names.txt を作り直せばこのあたりの処理は不要
