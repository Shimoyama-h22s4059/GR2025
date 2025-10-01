from Bio import SeqIO
from PIL import Image
from tqdm import tqdm
import numpy as np

import csv
import math
import os


dir_path = "./data/gds_dataset"  # データセットの場所
save_path = "./graphs/gradation"  # グラフ表示画像の保存先
filenames = [os.path.join(dir_path, file) for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]  # .txt のみ抽出

amino_vec = {
    "A": {"x":  0.99019942, "y": 2.29554027},
    "R": {"x": -7.38605815, "y": 1.30236133},
    "N": {"x": -4.01061596, "y": 2.98579296},
    "D": {"x": -2.04788011, "y": 1.43394109},
    "C": {"x":  2.18212092, "y": 2.05872491},
    "Q": {"x": -4.99366066, "y": 3.32616193},
    "E": {"x": -3.73512536, "y": 3.32397933},
    "G": {"x": -0.04937042, "y": 0.49755659},
    "H": {"x": -4.48215043, "y": 3.98877519},
    "I": {"x":  5.41644264, "y": 0.95506498},
    "L": {"x":  5.11141138, "y": 2.03063381},
    "K": {"x": -6.26454053, "y": 3.12338469},
    "M": {"x":  3.58295155, "y": 4.81273916},
    "F": {"x":  5.09870182, "y": 4.03153069},
    "P": {"x": -2.46839549, "y": 4.91497952},
    "S": {"x": -0.17443449, "y": 2.99492447},
    "T": {"x": -0.58046457, "y": 4.96619179},
    "W": {"x": -0.32567719, "y": 6.99241978},
    "Y": {"x": -2.00762263, "y": 6.70592659},
    "V": {"x":  4.82962913, "y": 1.29409523},
}

exclusion_bases = list("BJOUXZ")

size = 224
padding = 3
linewidth = 2


def check_valid_seq(seq):
    """
    有効なアミノ酸配列かどうかを返す関数
    :param seq: タンパク質配列
    :return: 有効なタンパク質ならば True
    """

    # 配列長が1000以上なら除外
    if len(seq) >= 1000:
        return False

    # "BJOUXZ" が含まれていたら除外
    for base in exclusion_bases:
        if base in seq:
            return False

    return True


def map_range(x, a, b, c, d):
    """
    変数 $x$ を 範囲 [$a$, $b$] から [$c$, $d$] にリマップします
    :param x: 変換する対象
    :param a: 変換前の下端
    :param b: 変換前の上端
    :param c: 変換後の下端
    :param d: 変換後の上端
    :return: リマップした値
    """
    return (x - a) / (b - a) * (d - c) + c


def draw_point(canvas, x: int, y: int, width: int, intensity: int):
    """
    点を描画します
    :param canvas: numpy の2次元配列
    :param x: 座標 $x$
    :param y: 座標 $y$
    :param width: 点の幅
    :param intensity: 点の白色の強度
    :return:
    """

    size = canvas.shape[0]

    for i in range(-width, width + 1):
        yi = y + i

        if 0 <= yi < size:
            for j in range(-width, width + 1):
                xi = x + j

                if 0 <= xi < size:
                    r = math.sqrt(i ** 2 + j ** 2)  # 中心からの距離

                    if r <= width:  # 半径内部かどうかを判定
                        val = int(intensity * (1 - r / width))  # 直線的に色を変化
                        # val = int((intensity / (r_0 + 1)) - 1)  # 中心から反比例するように色を変化

                        if val > canvas[yi, xi]:  # 画素よりも大きい値であれば上書き
                            canvas[yi, xi] = val


def drawline_with_bresenham_algorithm(canvas, x0: int, y0: int, x1: int, y1: int, width: int, intensity: int):
    """
    ブレゼンハムのアルゴリズムで2点間の直線を描画します
    :param canvas: numpy の2次元配列
    :param x0: 点 $x_0$
    :param y0: 点 $y_0$
    :param x1: 点 $x_1$
    :param y1: 点 $y_1$
    :param width 直線の幅
    :return: None
    """

    # ここで float を int に変換
    x0 = round(x0)
    y0 = round(y0)
    x1 = round(x1)
    y1 = round(y1)

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        draw_point(canvas, x0, y0, width, intensity)

        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x0 += sx

        if e2 < dx:
            err += dx
            y0 += sy

    draw_point(canvas, x1, y1, width, intensity)


def generate_graph(seq, accession_number, size, padding, width):
    """
    アミノ酸配列からグラフ表示画像を作成します
    :param seq: アミノ酸配列
    :param accession_number: アクセッション番号
    :param size: 画像サイズ
    :param padding: 画像のパディング
    :param width: 線幅
    :return:
    """

    x = y = 0
    x_min = x_max = 0
    y_min = y_max = 0

    points = [{"x": 0, "y": 0}]

    for c in seq:
        x += amino_vec[c]["x"]
        y += amino_vec[c]["y"]

        points.append({"x": x, "y": y})

        x_min, x_max = min(x, x_min), max(x, x_max)
        y_min, y_max = min(y, y_min), max(y, y_max)

    mapped_points = [
        {
            "x": map_range(point["x"], x_min, x_max, padding, (size - padding)),
            "y": map_range(point["y"], y_min, y_max, padding, (size - padding))
        }
        for point in points
    ]

    canvas = np.zeros((size, size), dtype=np.uint8)
    n_segments = len(mapped_points) - 1

    for i in range(n_segments):
        start, end = mapped_points[i], mapped_points[i + 1]

        progress = i / n_segments
        intensity = int(255 * progress)
        # draw.line([(start["x"], start["y"]), (end["x"], end["y"])], fill=255, width=3)
        drawline_with_bresenham_algorithm(canvas, start["x"], start["y"], end["x"], end["y"], width, intensity)

    img = Image.fromarray(canvas, mode="L")  # numpy 配列から画像を生成
    img.save(f"./{save_path}/{accession_number}.png")


number = 1  # ファイル名に使う通し番号

with open("./gpcr_labels.csv", "w", encoding="utf-8", newline="") as csv_file:  # ラベルをCSVファイルに保存
    csv_writer = csv.writer(csv_file)

    for filename in tqdm(filenames):
        # print(f"\033[33m[{filename}]\033[0m")

        class_name = filename.split("Class")[1][0]  # クラス名を取得

        with open(filename, "r", encoding="utf-8") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                accession_number = record.id.split("|")[3] if len(record.id.split("|")[3]) > 0 else "Unknown"  # アクセッション番号を取得
                seq = record.seq  # アミノ酸配列を取得

                if check_valid_seq(seq):  # 有効なアミノ酸配列かどうかを判定する
                    # print(f"\033[34m[{accession_number}]\033[0m")

                    generate_graph(seq, number, size, padding, linewidth)  # グラフを保存
                    csv_writer.writerow([number, class_name, accession_number])  # 一応アクセッション番号も含めて保存

                    number += 1

# テストデータ
# seq = "ACDEFGHIKLMNPQRSTVWY"
# generate_graph(seq, "test", size, padding, linewidth)


print("\033[32m✔ Completed! \033[0m")
