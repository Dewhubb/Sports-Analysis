# アントニ担当: 10チームの総合打率データ、チーム別の打率データと気温の関係の分析

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans JP', 'DejaVu Sans', 'Arial']

playerDF = pd.read_csv("players2.csv")

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

with open("analyze.csv", mode = "w", encoding = "utf-8", newline='') as file:
    writer = csv.writer(file, quoting = csv.QUOTE_NONE, delimiter='\t', escapechar='\t')
    writer.writerow(["エリア,打率,気温(°C)"])

    for key, value in teamNames.items():
        environmentDF = pd.read_csv(f"environment{key}.csv")

        gameDF = pd.read_csv(f"game{key}.csv")
        gameTimeDF = pd.read_csv(f"gameTime{key}.csv")

        environmentGameDF = pd.DataFrame(columns = environmentDF.columns)

        # 気象データ
        for row in gameTimeDF.itertuples():
            environmentDFBufferAppend = environmentDF[environmentDF["日付"] == row.matchID]
            environmentDFBufferAppend["時刻"] = environmentDFBufferAppend["時刻"].str[0:2].astype(int)
            environmentDFBufferAppend = environmentDFBufferAppend[(environmentDFBufferAppend["時刻"] >= row.開始時間) & (environmentDFBufferAppend["時刻"] <= row.終了時間)]
            environmentGameDF = (environmentDFBufferAppend if environmentGameDF.empty else pd.concat([environmentGameDF, environmentDFBufferAppend], ignore_index = True))

        environmentGameDF = environmentGameDF.groupby("日付")["気温(°C)"].mean()

        playersHitRateToTemp = []

        print(environmentGameDF)

        # 試合データ
        for row in gameDF.itertuples():
            currentName = row[2]
            currentHit = int(row[3])
            currentHitRate = float(row[5])
            currentDate = row[1]

            if (currentHit == 0):
                continue
        
            try:
                currentAvgTemp = environmentGameDF[int(currentDate)]
            except:
                continue

            area = playerDF.loc[(playerDF["名前"] == currentName) & (playerDF["チーム"] == value)].エリア

            writer.writerow([f"{area.iloc[0]},{currentHitRate},{currentAvgTemp}"])

for key, value in teamNames.items():
    with open(f"analyze{key}.csv", mode = "w", encoding = "utf-8", newline='') as file:
        writer = csv.writer(file, quoting = csv.QUOTE_NONE, delimiter='\t', escapechar='\t')
        writer.writerow(["エリア,打率,気温(°C)"])

        
        environmentDF = pd.read_csv(f"environment{key}.csv")

        gameDF = pd.read_csv(f"game{key}.csv")
        gameTimeDF = pd.read_csv(f"gameTime{key}.csv")

        environmentGameDF = pd.DataFrame(columns = environmentDF.columns)

        # 気象データ
        for row in gameTimeDF.itertuples():
            environmentDFBufferAppend = environmentDF[environmentDF["日付"] == row.matchID]
            environmentDFBufferAppend["時刻"] = environmentDFBufferAppend["時刻"].str[0:2].astype(int)
            environmentDFBufferAppend = environmentDFBufferAppend[(environmentDFBufferAppend["時刻"] >= row.開始時間) & (environmentDFBufferAppend["時刻"] <= row.終了時間)]
            environmentGameDF = (environmentDFBufferAppend if environmentGameDF.empty else pd.concat([environmentGameDF, environmentDFBufferAppend], ignore_index = True))

        environmentGameDF = environmentGameDF.groupby("日付")["気温(°C)"].mean()

        playersHitRateToTemp = []

        print(environmentGameDF)

        # 試合データ
        for row in gameDF.itertuples():
            currentName = row[2]
            currentHit = int(row[3])
            currentHitRate = float(row[5])
            currentDate = row[1]

            if (currentHit == 0):
                continue
        
            try:
                currentAvgTemp = environmentGameDF[int(currentDate)]
            except:
                continue

            area = playerDF.loc[(playerDF["名前"] == currentName) & (playerDF["チーム"] == value)].エリア

            writer.writerow([f"{area.iloc[0]},{currentHitRate},{currentAvgTemp}"])

data = pd.read_csv("analyze.csv")

hitRate = []
hitRate0 = pd.Series([])
hitRate1 = pd.Series([])
hitRate2 = pd.Series([])
temp = []
temp0 = pd.Series([])
temp1 = pd.Series([])
temp2 = pd.Series([])

for row in data.itertuples():
    hitRate.append(row[2])
    temp.append(row[3])

for binCount in range(4, 24, 2):
    bins = np.linspace(0, 35, binCount + 1)
    centers = (bins[:-1] + bins[1:]) / 2

    for row in data.itertuples():
        if (row[1] == 0):
            hitRate0 = pd.concat([hitRate0, pd.Series([row[2]])])
            temp0 = pd.concat([temp0, pd.Series([row[3]])])
        elif (row[1] == 1):
            hitRate1 = pd.concat([hitRate1, pd.Series([row[2]])])
            temp1 = pd.concat([temp1, pd.Series([row[3]])])
        else:
            hitRate2 = pd.concat([hitRate2, pd.Series([row[2]])])
            temp2 = pd.concat([temp2, pd.Series([row[3]])])

    hitRate0Assigned = np.digitize(temp0, bins)
    hitRate0Avgs = np.array([np.mean(hitRate0[hitRate0Assigned == i]) for i in range(1, len(bins))])
    hitRate1Assigned = np.digitize(temp1, bins)
    hitRate1Avgs = np.array([np.mean(hitRate1[hitRate1Assigned == i]) for i in range(1, len(bins))])
    hitRate2Assigned = np.digitize(temp2, bins)
    hitRate2Avgs = np.array([np.mean(hitRate2[hitRate2Assigned == i]) for i in range(1, len(bins))])

    plt.clf()
    plt.plot(centers, hitRate0Avgs, color = "#00587E", label = "寒い地域")
    plt.plot(centers, hitRate1Avgs, color = "#886400", label = "暖かい地域")
    plt.xlabel("気温(°C)")
    plt.ylabel("打率")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"Analyze_{binCount}Bins.png")

for binCount in range(4, 41, 4):
    plt.clf()
    plt.hist([temp0, temp1], bins = binCount, color = ["#00587E", "#886400"])
    plt.xlabel("気温(°C)")
    plt.ylabel("サンプル数")
    plt.savefig(f"Analyze_DataCount_{binCount}Bins.png")

for key, value in teamNames.items():
    data = pd.read_csv(f"analyze{key}.csv")

    hitRate = []
    hitRate0 = pd.Series([])
    hitRate1 = pd.Series([])
    hitRate2 = pd.Series([])
    temp = []
    temp0 = pd.Series([])
    temp1 = pd.Series([])
    temp2 = pd.Series([])

    for row in data.itertuples():
        hitRate.append(row[2])
        temp.append(row[3])

    for binCount in range(4, 24, 2):
        bins = np.linspace(0, 35, binCount + 1)
        centers = (bins[:-1] + bins[1:]) / 2

        for row in data.itertuples():
            if (row[1] == 0):
                hitRate0 = pd.concat([hitRate0, pd.Series([row[2]])])
                temp0 = pd.concat([temp0, pd.Series([row[3]])])
            elif (row[1] == 1):
                hitRate1 = pd.concat([hitRate1, pd.Series([row[2]])])
                temp1 = pd.concat([temp1, pd.Series([row[3]])])
            else:
                hitRate2 = pd.concat([hitRate2, pd.Series([row[2]])])
                temp2 = pd.concat([temp2, pd.Series([row[3]])])

        hitRate0Assigned = np.digitize(temp0, bins)
        hitRate0Avgs = np.array([np.mean(hitRate0[hitRate0Assigned == i]) for i in range(1, len(bins))])
        hitRate1Assigned = np.digitize(temp1, bins)
        hitRate1Avgs = np.array([np.mean(hitRate1[hitRate1Assigned == i]) for i in range(1, len(bins))])
        hitRate2Assigned = np.digitize(temp2, bins)
        hitRate2Avgs = np.array([np.mean(hitRate2[hitRate2Assigned == i]) for i in range(1, len(bins))])

        plt.clf()
        plt.plot(centers, hitRate0Avgs, color = "#00587E", label = "寒い地域")
        plt.plot(centers, hitRate1Avgs, color = "#886400", label = "暖かい地域")
        plt.xlabel("気温(°C)")
        plt.ylabel("打率")
        plt.grid(True)
        plt.legend()
        plt.savefig(f"Analyze_{key}_{binCount}Bins.png")

    for binCount in range(4, 41, 4):
        plt.clf()
        plt.hist([temp0, temp1], bins = binCount, color = ["#00587E", "#886400"])
        plt.xlabel("気温(°C)")
        plt.ylabel("サンプル数")
        plt.savefig(f"Analyze_{key}_DataCount_{binCount}Bins.png")