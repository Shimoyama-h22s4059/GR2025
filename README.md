# GR2025

## TL;DR
卒業研究用のリポジトリです

## 使用ライブラリ
以下の通りです

| 名前 | バージョンなど |
| :-- | :-- |
| Python | 3.13.3 |
| PyTorch | 2.7.1+cu118 |
| torchvision | 2.7.1+cu118 |
| huggingface_hub | 0.33.4 |

## 使用したTransformerモデル
- [`google/vit-base-patch16-224-in21k`](https://huggingface.co/google/vit-base-patch16-224-in21k)

## 更新履歴

### 2025/07/20
- 機械学習の基礎を学びました
- HuggingFaceの `datasets` を用いてMNISTデータセットを学習させました
- Google Colab でも動かしてみましたが、無料枠では限界を感じました
  - 研究するなら金払え！！！！
  - <img width="288" height="215" alt="{5880D043-7314-4998-8BEC-A9F857CCEFBB}" src="https://github.com/user-attachments/assets/e572d875-77d1-4b93-98cf-efae1a635d5a" />
- PyTorch を動かすのにPythonのバージョンをあれこれ揃えないといけない

### 2025/07/21
- 昨日、HuggingFaceおよびPyTorchを用いた学習方法を学んだので、少し動かしてみた
- MNISTの学習に4時間程度要しました
  - epoch: 3
  - batch size: 64
- 手書き文字認識する簡単なWebアプリを実装
- Flask で作成、`app.py` にて実行可能

### 2025/10/29
- 一旦ハイパーパラメータの調整をする方針で進める
- 埋め込みベクトルを取得して画像生成する手法もやる
