# ファイル名：Environment_Graph.py
# 作成者：ディウ
# 試合データと環境データを組み合わせ、打率と気象条件（気温・湿度・日照時間・視程・天気）の関係を
# 分析・可視化するプログラム

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# ----------------------------------------------------------
# 【1】データ読み込み
# ----------------------------------------------------------
# 試合データ、試合時間データ、環境データ（広島の気象庁データ）を読み込む。

game_df = pd.read_csv('Data/game.csv', encoding='utf-8') 
gameTime_df = pd.read_csv('Data/gameTime.csv', encoding='utf-8')
env_df = pd.read_csv('Data/Ver2/environmentHiroshima.csv', encoding='utf-8')

# ----------------------------------------------------------
# 【2】不要データ削除
# ----------------------------------------------------------

game_df = game_df[game_df['打数'] > 0] 

# ----------------------------------------------------------
# 【3】試合ごとの平均打率を計算
# ----------------------------------------------------------

game_df = game_df.groupby('matchID')['打率'].mean().reset_index()   # matchIDごとにグループ化し、平均打率を求める。
game_df['打率'] = game_df['打率'] * 100   # 打率を100倍して「%」表現に変換。

# ----------------------------------------------------------
# 【4】試合時間データの整形
# ----------------------------------------------------------
# 「時間帯」列を「開始時間」と「終了時間」に分割する。

gameTime_df["時間帯"] = gameTime_df["時間帯"].str.replace(" ", "")
gameTime_df[["開始時間", "終了時間"]] = gameTime_df["時間帯"].str.split("-", expand=True)
gameTime_df["開始時間"] = gameTime_df["開始時間"].astype(int)
gameTime_df["終了時間"] = gameTime_df["終了時間"].astype(int)
gameTime_df = gameTime_df.drop(columns=["時間帯"])

# ----------------------------------------------------------
# 【5】打率データと試合時間データを結合
# ----------------------------------------------------------
# 同じ試合ID（matchID）でデータを結び付ける。

game_df = pd.merge(game_df, gameTime_df, on='matchID')

# ----------------------------------------------------------
# 【6】環境データの整形
# ----------------------------------------------------------
# 日付・時刻を数値化して扱いやすくする。

env_df['時刻'] = env_df['時刻'].str[:2].astype(int)
env_df['日付'] = env_df['日付'].astype(int)

# ----------------------------------------------------------
# 【7】環境データと試合データを結合
# ----------------------------------------------------------
# 試合の日付をキーにして結合する。

env_df = pd.merge(env_df, game_df, left_on="日付", right_on='matchID')

# ----------------------------------------------------------
# 【8】試合中の時間帯のデータだけを抽出
# ----------------------------------------------------------
# その日のうち、試合開始〜終了の範囲に含まれる気象データだけ残す。

env_df = env_df[(env_df['時刻'] >= env_df['開始時間']) & (env_df['時刻'] <= env_df['終了時間'])]

# ----------------------------------------------------------
# 【9】不要な列を削除し、整理する。
# ----------------------------------------------------------

env_df = env_df.drop(columns=['時刻', 'matchID', '開始時間', '終了時間'])

# ----------------------------------------------------------
# 【10】同じ日付ごとにまとめる（リスト化）
# ----------------------------------------------------------
# 各日付のデータを集め、1日の気象条件をリストにまとめる。

env_df['視程(km)'] = env_df['視程(km)'].fillna(0.0)
env_df['日照時間(h)'] = env_df['日照時間(h)'].fillna(0.0).astype(float)
df = env_df.groupby('日付').agg(list).reset_index()

# ----------------------------------------------------------
# 【11】数値データの平均値を計算
# ----------------------------------------------------------
# 気温・湿度・日照時間・視程・打率の平均を1日ごとに出す。

numeric_cols = ['気温(°C)', '湿度(%)', '日照時間(h)', '視程(km)', '打率']
for col in numeric_cols:
    df[col] = df[col].apply(lambda x: sum(x)/len(x) if isinstance(x, list) and len(x) > 0 else None)

# ----------------------------------------------------------
# 【12】天気の最頻値（モード）を取得
# ----------------------------------------------------------
# その日で一番多かった天気（晴れ・曇りなど）を代表値として使う。

df['最頻天気'] = df['天気'].apply(lambda x: Counter(x).most_common(1)[0][0] if isinstance(x, list) else None)

# ----------------------------------------------------------
# 【13】列名を英語に変換（グラフ用）
# ----------------------------------------------------------

df = df.rename(columns={
    '打率': 'batting',
    '気温(°C)': 'avg_temp',
    '湿度(%)': 'avg_humidity',
    '日照時間(h)': 'avg_insolation',
    '視程(km)': 'avg_visibility'
})

# ==========================================================
# 【14】各気象条件との関係を可視化
# 　→ 気温・湿度・日照時間・視程・天気と打率の関係を分析・表示する
# ==========================================================

# ----------------------------------------------------------
# 【15】気温と打率の関係の可視化 (散布図)
# ----------------------------------------------------------
plt.figure(figsize=(12, 6))
plt.scatter(df['avg_temp'], df['batting'], color="#4BA322", s=60, edgecolors="#000000", alpha=0.8, linewidths=1) # 散布図
z = np.polyfit(df['avg_temp'], df['batting'], 1) # 1次回帰
p = np.poly1d(z)
plt.plot(df['avg_temp'], p(df['avg_temp']), color="#DC1111DC", linewidth=2, label="トレンドライン") # 回帰曲線
plt.legend(fontsize=40, prop={"family": "UD Digi Kyokasho N"}, loc="upper right")
plt.xlim(min(df['avg_temp']) + 2, max(df['avg_temp']) + 2)
x_ticks = np.arange(int(min(df['avg_temp'])) - 2, int(max(df['avg_temp'])) + 3, 2)
y_ticks = np.arange(0.0, 101, 10)
plt.xticks(x_ticks, fontsize=12)
plt.yticks(y_ticks, fontsize=12)
plt.xlabel("気温 [℃]", fontsize=15, fontname="UD Digi Kyokasho N")
plt.ylabel("打率 [%]", fontsize=15, fontname="UD Digi Kyokasho N")
plt.title("打率と気温の関係 (2025年3月28日〜10月4日)", fontsize=16, fontname="UD Digi Kyokasho N")
plt.grid(color="gray", linestyle="--", linewidth=1, alpha=0.6)
plt.tight_layout()
plt.savefig('Outputs/Dew/Temperature.png')
plt.show()
# ----------------------------------------------------------
# 【16】湿度と打率の関係の可視化 (散布図)
# ----------------------------------------------------------

plt.figure(figsize=(12, 6))
plt.scatter(df['avg_humidity'], df['batting'], color="#1A50E4", edgecolors="#000000", s=60, alpha=0.8, linewidths=1)
z = np.polyfit(df['avg_humidity'], df['batting'], 1) # 1次回帰（線形）
p = np.poly1d(z)
plt.plot(df['avg_humidity'], p(df['avg_humidity']), color="#FF7700DC", linewidth=2, label="トレンドライン")
plt.legend(fontsize=40, prop={"family": "UD Digi Kyokasho N"}, loc="upper right")
plt.xlim(0, 100)
x_ticks = np.arange(0, 101, 10)
y_ticks = np.arange(0.0, 101, 10)
plt.xticks(x_ticks, fontsize=12)
plt.yticks(y_ticks, fontsize=12)
plt.xlabel("湿度 [%]", fontsize=15, fontname="UD Digi Kyokasho N")
plt.ylabel("打率 [%]", fontsize=15, fontname="UD Digi Kyokasho N")
plt.title("打率と湿度の関係 (2025年3月28日〜2025年10月4日)", fontsize=16, fontname="UD Digi Kyokasho N")
plt.grid(color="gray", linestyle="--", linewidth=1, alpha=0.6)
plt.tight_layout()
plt.savefig('Outputs/Dew/Humidity.png')
plt.show()

# ----------------------------------------------------------
# 【17】日照時間と打率の関係の可視化 (散布図)
# ----------------------------------------------------------

plt.figure(figsize=(12, 6))
plt.scatter(df['avg_insolation'], df['batting'], color="#E67E22", edgecolors="#000000", s=60, alpha=0.8, linewidths=1)
z = np.polyfit(df["avg_insolation"], df['batting'], 1) # 1次回帰
p = np.poly1d(z)
plt.plot(df['avg_insolation'], p(df['avg_insolation']), color="#2E86C1", linewidth=2, label="トレンドライン")
plt.legend(fontsize=35, prop={"family": "UD Digi Kyokasho N"}, loc="upper right")
plt.xlim(-0.05, 1.05)
x_ticks = np.arange(0, 1.1, 0.1)
y_ticks = np.arange(0.0, 101, 10)
plt.xticks(x_ticks, fontsize=12)
plt.yticks(y_ticks, fontsize=12)
plt.xlabel(" 1 時間あたりの日照時間 [h]", fontsize=15, fontname="UD Digi Kyokasho N")
plt.ylabel("打率 [%]", fontsize=15, fontname="UD Digi Kyokasho N")
plt.title("打率と 1 時間あたりの日照時間の関係 (2025年3月28日〜2025年10月4日)", fontsize=16, fontname="UD Digi Kyokasho N")
plt.grid(color="gray", linestyle="--", linewidth=1, alpha=0.6)
plt.tight_layout()
plt.savefig('Outputs/Dew/Insolation.png')
plt.show()

# ----------------------------------------------------------
# 【18】視程と打率の関係の可視化 (散布図)
# ----------------------------------------------------------

plt.figure(figsize=(12, 6))
plt.scatter(df['avg_visibility'], df['batting'], color="#2E86C1", edgecolors="#000000", s=60, alpha=0.8, linewidths=1)
z = np.polyfit(df['avg_visibility'], df['batting'], 1) # 1次回帰
p = np.poly1d(z)
plt.plot(df['avg_visibility'], p(df['avg_visibility']), color="#1ABC9C", linewidth=2, label="トレンドライン")
plt.legend(fontsize=35, prop={"family": "UD Digi Kyokasho N"}, loc="upper right")
plt.xlim(min(df['avg_visibility'])-0.5, max(df['avg_visibility'])+0.5)
x_ticks = np.arange(int(min(df['avg_visibility'])), int(max(df['avg_visibility']))+0.5, 1.0)
y_ticks = np.arange(0.0, 101, 10)
plt.xticks(x_ticks, fontsize=12)
plt.yticks(y_ticks, fontsize=12)
plt.xlabel("視程 [km]", fontsize=15, fontname="UD Digi Kyokasho N")
plt.ylabel("打率 [%]", fontsize=15, fontname="UD Digi Kyokasho N")
plt.title("打率と視程の関係 (2025年3月28日〜2025年10月4日)", fontsize=16, fontname="UD Digi Kyokasho N")
plt.grid(color="gray", linestyle="--", linewidth=1, alpha=0.6)
plt.tight_layout()
plt.savefig('Outputs/Dew/Visibility.png')
plt.show()


# ----------------------------------------------------------
# 【19】天気と打率の関係の可視化 (箱ひげ図)
# ----------------------------------------------------------

plt.figure(figsize=(8, 6))
weather_groups = df.groupby('最頻天気')['batting'].apply(list)

bp = plt.boxplot(weather_groups, labels=weather_groups.index, patch_artist=True, widths=0.3, whis=(0, 100))

box_colors = ['peachpuff', 'orange', 'tomato', 'skyblue']
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color)
    
for median_line in bp['medians']:
    median_line.set(color='black')
    
y_ticks = np.arange(0.0, 101, 10)
plt.xticks(fontname="UD Digi Kyokasho N", fontsize=15)
plt.yticks(y_ticks, fontsize=12)
plt.xlabel("天気", fontsize=15, fontname="UD Digi Kyokasho N")
plt.ylabel("打率 [%]", fontsize=15, fontname="UD Digi Kyokasho N")
plt.title("打率と天気の関係 (2025年3月28日〜2025年10月4日)", fontsize=16, fontname="UD Digi Kyokasho N")
plt.grid(color="gray", linestyle="--", linewidth=1, alpha=0.6)
plt.tight_layout()
plt.savefig('Outputs/Dew/Weather.png')
plt.show()
