# kaken_trans
NII 科研費データをよしなに変換
- "各年度配分額" にまとめて記入されている年度ごと配分額を、"各年度配分額.年度" と "各年度配分額.配分額" にそれぞれ分解して別レコード行にする
- "研究代表者" を "研究代表者.氏名", "研究代表者.所属",  "研究代表者.学部", "研究代表者.職階", "研究代表者.研究者番号" の各カラムに分解
- "審査区分" を "審査区分.コード" と "審査区分.分野名" の各カラムに分解

## Usage
科学研究費助成事業データベース https://kaken.nii.ac.jp の検索結果 CSV を引数ファイル名で読み込んで xlsx を吐く
> python3 kaken_trans.py kaken.nii.ac.jp_2022-03-23_00-39-33.csv