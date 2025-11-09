# ファイル名：Environment_Graph.py
# 作成者：ディウ（Pitipat Wattananantapan）
# 作成日：2025年11月3日
# 内容：試合データと環境データを組み合わせ、打率と気象条件（気温・湿度・日照時間・視程・天気）の関係を分析・可視化するプログラム

import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import os
from collections import Counter

# ----------------------------------------------------------
# データ読み込み
# ----------------------------------------------------------

game_df = pd.read_csv('Data/game.csv', encoding='utf-8') # 試合成績データ（打数・打率など）
gameTime_df = pd.read_csv('Data/gameTime.csv', encoding='utf-8') # 試合時間データ（時間帯）
env_df = pd.read_csv('Data/Environment_Data.csv', encoding='utf-8') # 環境データ（気温・湿度・日照時間・視程・天気）

# ----------------------------------------------------------
# 打数が0の行を除外（打率計算に不要なデータを削除）
# ----------------------------------------------------------

game_df = game_df[game_df['打数'] > 0]

# ----------------------------------------------------------
# matchIDごとに平均打率を計算
# ----------------------------------------------------------

game_df = game_df.groupby('matchID')['打率'].mean().reset_index()
game_df['打率'] = game_df['打率'] * 100
print(game_df)


# ----------------------------------------------------------
# 試合時間データの加工
# ----------------------------------------------------------

gameTime_df["時間帯"] = gameTime_df["時間帯"].str.replace(" ", "") # 空白削除
gameTime_df[["開始時間", "終了時間"]] = gameTime_df["時間帯"].str.split("-", expand=True) # 開始・終了時間を分割
gameTime_df["開始時間"] = gameTime_df["開始時間"].astype(int)
gameTime_df["終了時間"] = gameTime_df["終了時間"].astype(int)
gameTime_df = gameTime_df.drop(columns=["時間帯"]) # 不要列削除

# ----------------------------------------------------------
# 打率データと試合時間データを結合
# ----------------------------------------------------------

game_df = pd.merge(game_df, gameTime_df, on='matchID')

# ----------------------------------------------------------
# 環境データの加工
# ----------------------------------------------------------

env_df['時刻'] = env_df['時刻'].str[:2].astype(int) # 時刻列から時間のみを抽出して整数型に変換
env_df['日付'] = env_df['日付'].astype(str).apply(lambda x: f"{x[:4]}{int(x[4:6])}{int(x[6:])}") # 日付を整形 2025410
env_df['日付'] = env_df['日付'].astype(int)
# ----------------------------------------------------------
# 日付(matchID)で打率データと環境データを結合
# ----------------------------------------------------------

env_df = pd.merge(env_df, game_df, left_on="日付", right_on='matchID')

# ----------------------------------------------------------
# 時刻が試合開始～終了の範囲内のデータのみ抽出
# ----------------------------------------------------------

env_df = env_df[(env_df['時刻'] >= env_df['開始時間']) & (env_df['時刻'] <= env_df['終了時間'])]

#----------------------------------------------------------
# 不要列を削除
# ----------------------------------------------------------

env_df = env_df.drop(columns=['時刻', 'matchID', '開始時間', '終了時間'])

# ----------------------------------------------------------
# 日付ごとにまとめてリスト化
# ----------------------------------------------------------

df = env_df.groupby('日付').agg(list).reset_index()

# ----------------------------------------------------------
# 数値列の平均値を計算
# ----------------------------------------------------------

numeric_cols = ['気温(°C)', '湿度(%)', '日照時間(h)', '視程(km)', '打率']
for col in numeric_cols:
    df[col] = df[col].apply(lambda x: sum(x)/len(x) if isinstance(x, list) and len(x) > 0 else None)

# ----------------------------------------------------------
# 天気の最頻値（モード）を取得
# ----------------------------------------------------------

df['最頻天気'] = df['天気'].apply(lambda x: Counter(x).most_common(1)[0][0] if isinstance(x, list) else None)

# ----------------------------------------------------------
# グラフ用に列名を変更
# ----------------------------------------------------------

df = df.rename(columns={
'打率': 'batting',
'気温(°C)': 'avg_temp',
'湿度(%)': 'avg_humidity',
'日照時間(h)': 'avg_insolation',
'視程(km)': 'avg_visibility'
})

# ----------------------------------------------------------
# 【7】気温と打率の関係の可視化
# ----------------------------------------------------------
absolute_directory = "C:\Users\acer\Documents\Sports-Analysis-Cloned\Outputs\Dew"  # Example absolute path

plt.figure(figsize=(12, 6))
plt.scatter(df['avg_temp'], df['batting'], color="#4BA322", s=60, edgecolors="#000000", alpha=0.8, linewidths=1) # 散布図
z = np.polyfit(df['avg_temp'], df['batting'], 1) # 1次回帰
p = np.poly1d(z)
plt.plot(df['avg_temp'], p(df['avg_temp']), color="#DC1111DC", linewidth=2, label="トレンドライン") # 回帰曲線
plt.legend(fontsize=40, prop={"family": "UD Digi Kyokasho N"}, loc="upper right")

plt.ylim(0.0, 1.0)
plt.xlim(min(df['avg_temp']) + 2, max(df['avg_temp']) + 2)
x_ticks = np.arange(int(min(df['avg_temp'])) - 2, int(max(df['avg_temp'])) + 3, 2)
y_ticks = np.arange(0.0, 101, 10)
plt.xticks(x_ticks)
plt.yticks(y_ticks)
plt.ylabel("打率 [%]", fontsize=15, fontname="UD Digi Kyokasho N")
plt.xlabel("気温 [℃]", fontsize=15, fontname="UD Digi Kyokasho N")
plt.title("打率と気温の関係 (2025年3月28日〜10月4日)", fontsize=16, fontname="UD Digi Kyokasho N")
plt.grid(color="gray", linestyle="--", linewidth=1, alpha=0.6)
plt.tight_layout()
full_path = os.path.join(absolute_directory, "Temperature.png")
plt.savefig(full_path)
plt.show()