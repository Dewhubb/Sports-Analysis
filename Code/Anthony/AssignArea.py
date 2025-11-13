# アントニ担当: 各選手の出身地からエリアを分類して格納
# エリア0は比較的寒い地域、1は平均的な地域、2は例外（海外出身）

import pandas as pd
import csv

playersDF = pd.read_csv("Data/Ver2/players.csv")

i = 0
with open("Data/Ver2/players.csv", mode = "w", encoding = "utf-8", newline='') as file:
    writer = csv.writer(file, quoting = csv.QUOTE_NONE, delimiter='\t')
    writer.writerow(["名前,チーム,地域,エリア"])
    for player in playersDF.itertuples():
        if (player.地域 in ["北海道","青森","岩手","秋田","宮城","山形","福島","新潟","富山","石川","福井","長野"]):
            playersDF.loc[i, "エリア"] = val = 0
        elif (len(player.地域) <= 3):
            playersDF.loc[i, "エリア"] = val = 1
        else:
            playersDF.loc[i, "エリア"] = val = 2
        i += 1
        print(player.地域, len(player.地域))
        writer.writerow([f"{player.名前},{player.チーム},{player.地域},{val}"])