from Bio import SeqIO
from PIL import Image, ImageDraw

import csv
import os

dir_path = "./data/gds_dataset"  # ディレクトリ
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
padding = 10


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


def generate_graph(seq, accession_number, size, padding):
    """
    アミノ酸配列からグラフ表示画像を作成します
    :param seq: アミノ酸配列
    :param accession_number: アクセッション番号
    :param size: 画像サイズ
    :param padding: 画像のパディング
    :return:
    """
    x = 0
    y = 0

    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0

    points = [{"x": 0, "y": 0}]

    for c in seq:
        x += amino_vec[c]["x"]
        y += amino_vec[c]["y"]

        points.append({"x": x, "y": y})

        x_min = min(x, x_min)
        x_max = max(x, x_max)
        y_min = min(y, y_min)
        y_max = max(y, y_max)

    mapped_points = [
        {
            "x": map_range(point["x"], x_min, x_max, padding, (size - padding)),
            "y": map_range(point["y"], y_min, y_max, padding, (size - padding))
        }
        for point in points
    ]

    img = Image.new("L", (size, size), color=0)  # (size * size) の黒画像で初期化
    draw = ImageDraw.Draw(img)  # 描画用オブジェクト

    for i in range(len(mapped_points) - 1):
        start = mapped_points[i]
        end = mapped_points[i + 1]

        draw.line([(start["x"], start["y"]), (end["x"], end["y"])], fill=255)

    img.save(f"./graphs/{accession_number}.png")


number = 1  # ファイル名に使う通し番号

with open("./gpcr_labels.csv", "w", encoding="utf-8", newline="") as csv_file:  # ラベルをCSVファイルに保存
    csv_writer = csv.writer(csv_file)

    for filename in filenames:
        print(f"\033[33m[{filename}]\033[0m")

        class_name = filename.split("Class")[1][0]  # クラス名を取得

        with open(filename, "r", encoding="utf-8") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                accession_number = record.id.split("|")[3] if len(record.id.split("|")[3]) > 0 else "Unknown"  # アクセッション番号を取得
                seq = record.seq  # アミノ酸配列を取得

                if check_valid_seq(seq):  # 有効なアミノ酸配列かどうかを判定する
                    print(f"\033[34m[{accession_number}]\033[0m")

                    generate_graph(seq, number, size, padding)  # グラフを保存
                    csv_writer.writerow([number, class_name, accession_number])  # 一応アクセッション番号も含めて保存

                    number += 1

print("\033[32m✔ Completed! \033[0m")
