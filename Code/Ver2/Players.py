# アントニ担当: 各選手のリストの作成
# 地域はファイル出力後、手動で検索し記入する。
# エリアはAssignArea.pyを使用して特定する。

import pandas as pd
import numpy as np
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

with open("players.csv", mode = "w", encoding = "utf-8", newline='') as file:
    writer = csv.writer(file, quoting = csv.QUOTE_NONE, delimiter='\t')
    writer.writerow(["名前,チーム,地域,エリア"])

    for key, value in teamNames.items():
        gameDF = pd.read_csv(f"game{key}.csv")

        players = []

        for row in gameDF.itertuples():
            currentName = row[2]
            if (currentName in players or int(row[3]) == 0):
                continue
            players.append(currentName)

        for i in range(len(players)):
            print(players[i])
            writer.writerow([f"{players[i]},{value},"])