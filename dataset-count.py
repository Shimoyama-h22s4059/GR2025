from Bio import SeqIO
from PIL import Image, ImageDraw, ImageFilter
from tqdm import tqdm

import csv
import os

dir_path = "./data/gds_dataset"  # ディレクトリ
filenames = [os.path.join(dir_path, file) for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]  # .txt のみ抽出

exclusion_bases = list("BJOUXZ")

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


total_seqs = 0
lens = []
count = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}


for filename in tqdm(filenames):
    class_name = filename.split("Class")[1][0]  # クラス名を取得
    
    with open(filename, "r", encoding="utf-8") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            accession_number = record.id.split("|")[3] if len(record.id.split("|")[3]) > 0 else "Unknown"  # アクセッション番号を取得
            seq = record.seq  # アミノ酸配列を取得

            if check_valid_seq(seq):  # 有効なアミノ酸配列かどうかを判定する
                # print(f"\033[34m[{accession_number}]\033[0m")

                total_seqs += len(seq)
                lens.append(seq)
                count[class_name] += 1

print("Total Seq:", total_seqs)
print(count)
print("\033[32m✔ Completed! \033[0m")
