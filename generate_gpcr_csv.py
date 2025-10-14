from Bio import SeqIO
import csv
import os
from tqdm import tqdm

data_dir = "./data/gds_dataset"
save_to = "./data/gpcr_dataset.csv"

files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".txt")]  # .txt ファイルを全て取得
files.sort()

num = 0

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


with open(save_to, "w", encoding="utf-8", newline="") as file:
    csv_file = csv.writer(file)
    csv_file.writerow(["id", "seq", "class"])
    
    for filename in tqdm(files):
        class_name = filename.split("Class")[1][0]  # クラス名を取得
    
        with open(filename, "r", encoding="utf-8") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                seq = record.seq
                
                if check_valid_seq(seq):
                    num += 1
                    csv_file.writerow([num, seq, class_name])

print("Total seq:", num)
print("\033[32m✔ Completed! \033[0m")
