# アントニ担当: 全試合の野球場リストの作成

import pandas as pd
import csv

teamNames = {"Hiroshima": "広島東洋カープ",
             "Hokkaido": "北海道日本ハムファイターズ",
             "Fukuoka": "福岡ソフトバンクホークス",
             "Hanshin": "阪神タイガース",
             "Yomiuri": "読売ジャイアンツ",
             "DeNA": "横浜DeNAベイスターズ",
             "Yakult": "東京ヤクルトスワローズ",
             "Chiba": "千葉ロッテマリーンズ",
             "Rakuten": "東北楽天ゴールデンイーグルス",
             "Saitama": "埼玉西武ライオンズ"}

stadiums = []

for key, value in teamNames.items():
    gameDF = pd.read_csv(f"Data/Ver3/gameStadium{key}.csv")
    for row in gameDF.itertuples():
        currentStadium = row[2]
        if (currentStadium not in stadiums):
            stadiums.append(currentStadium)

with open("Data/Ver3/stadiumList.csv", mode = "w", encoding = "utf-8", newline='') as file:
    writer = csv.writer(file, quoting = csv.QUOTE_NONE, delimiter='\t', escapechar='\t')
    writer.writerow(["球場,prec_no,block_no"])
    for i in stadiums:
        writer.writerow([i + ",,"])