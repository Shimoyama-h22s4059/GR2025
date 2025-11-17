# 独自データセットの作成

## 使用データセット
- 以下のデータセットを用いた
- 配列長 $L \geq 1000$ のものと `BJOUXZ` を含むものを除外

### [BIAS-PROFS](https://www.cs.kent.ac.uk/projects/biasprofs/)
- ファミリの配列数 10 以下のものを除外

### [InterPro](https://www.ebi.ac.uk/interpro/)
- Reviewed のみを用いた
  - Class A: [G protein-coupled receptor, rhodopsin-like (IPR000276)](https://www.ebi.ac.uk/interpro/entry/InterPro/IPR000276/)
  - Class B: [GPCR, family 2, secretin-like (IPR000832)](https://www.ebi.ac.uk/interpro/entry/InterPro/IPR000832/)
  - Class C: [GPCR, family 3 (IPR000337)](https://www.ebi.ac.uk/interpro/entry/InterPro/IPR000337/)
  - Class D:
    - [GPCR fungal pheromone mating factor, STE2 (IPR000366)](https://www.ebi.ac.uk/interpro/entry/InterPro/IPR000366/)
    - [GPCR fungal pheromone mating factor, STE3 (IPR001499)](https://www.ebi.ac.uk/interpro/entry/InterPro/IPR001499/)
  - Class E: [GCR1-cAMP receptor (IPR022343)](https://www.ebi.ac.uk/interpro/entry/InterPro/IPR022343/)
  - Class F: [Frizzled/Smoothened, 7TM (IPR000539)](https://www.ebi.ac.uk/interpro/entry/InterPro/IPR000539/)
