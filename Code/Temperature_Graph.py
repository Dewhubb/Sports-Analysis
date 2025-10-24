import numpy as np
import matplotlib.pyplot as plt
import csv 
import os

# 出力フォルダを確認して作成

os.makedirs('output', exist_ok=True)

# --- Step 1: 温度データの読み込み ---
temperature = np.array([])
with open('data/Environment.csv', mode='r', encoding='utf-8') as file:
    csvFile = csv.reader(file)
    next(csvFile)  # ヘッダーをスキップ
    for lines in csvFile:
        temperature = np.append(temperature, float(lines[3]))  # 4列目のデータを取得
        temperature.sort()

# --- Step 2: テスト用の打率データ（後で置き換え予定） ---

rng = np.random.default_rng()
daritsu = rng.standard_normal(len(temperature))  # 仮の打率データ
daritsu = np.round(daritsu, 4)  # 小数4桁で丸める

# --- Step 3: プロット ---
plt.figure(figsize=(8, 5))
plt.plot(temperature, daritsu, color='blue', marker='o', linestyle='dashed', linewidth=2, markersize=5)
plt.ylabel("打率", fontsize=14, fontname="UD Digi Kyokasho N")
plt.xlabel("気温 (℃)", fontsize=14, fontname="UD Digi Kyokasho N")
plt.title("打率と気温の関係（テストデータ）", fontsize=14, fontname="UD Digi Kyokasho N")
plt.grid(True)

plt.savefig('output/Temperature.png')
plt.show()
