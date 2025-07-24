from Bio import SeqIO
import os

dir_path = "./data/gds_dataset"  # ディレクトリ
filenames = [os.path.join(dir_path, file) for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]  # .txt のみ抽出

dictionary = {}
total_bases = 0
valid_records = 0

exclusion_bases = list("BJOUXZ")

accession_numbers = []

def check_valid_seq(seq):
    """
    有効なタンパク質かどうかを返す関数
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

for filename in filenames:
    print(f"\033[33m[{filename}]\033[0m")

    with open(filename, "r", encoding="utf-8") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            accession_number = record.id.split("|")[3]
            seq = record.seq

            if check_valid_seq(seq) and len(accession_number) > 0:
                accession_numbers.append(accession_number)
                valid_records += 1

                for c in seq:
                    dictionary.setdefault(c, 0)
                    dictionary[c] += 1
                    total_bases += 1

dictionary = sorted(dictionary.items())
accession_numbers.sort()
accession_numbers = set(accession_numbers)

print(dictionary)
print(f"valid_records = {valid_records}")
print(f"total_bases = {total_bases}")
print(f"len(accession_numbers) = {len(accession_numbers)}")

with open("./valid_accession_numbers.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(accession_numbers))
