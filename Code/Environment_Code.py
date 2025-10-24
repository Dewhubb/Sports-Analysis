# --------Environment_Code.py--------
# 環境データ自動収集プログラム
# 目的：気象庁の公式サイトから、指定された日付範囲の気象データを自動取得し、
#       CSVファイルに保存する。
# 使用技術：Python + Selenium
# -----------------------------------

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

# ChromeDriver のパスを指定
chrome_driver_path = 'C:/chrome-win64/chrome-win64'

# Chrome のオプション設定
chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")  # ウィンドウサイズを指定

# ChromeDriver サービスの作成
service = Service(chrome_driver_path)

# CSV のヘッダー（列名）を定義
columnLabel = [
    "日付", "時刻", "降水量(mm)", "気温(°C)", "露点温度(°C)", "蒸気圧(hPa)", 
    "湿度(%)", "風速(m/s)", "風向", "日照時間(h)", "全天日射量(MJ/㎡)", 
    "天気", "視程(km)"
]

# カラムラベルを画面に表示（確認用）
#print(columnLabel)

# CSV ファイルを新規作成して書き込み開始
with open("Data/Environment.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(columnLabel)  # ヘッダーを書き込む

    # Chromeドライバーの起動
    driver = webdriver.Chrome(options=chrome_options)

    # 3月～11月までの日付をループ処理
    for month in range(3, 12):
        for day in range(1, 31):
            
            # 気象庁サイトの特定日のURLを生成
            url = f"https://www.data.jma.go.jp/stats/etrn/view/hourly_s1.php?prec_no=67&block_no=47765&year=2025&month={month}&day={day}&view="
            driver.get(url)  # ページを開く

            time.sleep(3)  # ページが完全に読み込まれるまで待機

            # データ表のセルを取得（tdタグのうち class に 'data_0_0' を含む要素）
            cells = driver.find_elements(By.XPATH, "//td[contains(@class, 'data_0_0')]")

            # 各時間帯（1時間ごと）のデータを抽出
            for i in range(int(len(cells) / 16)):  # 1行あたり16列のデータがある
                date = f"2025-{month:02d}-{day:02d}"  # 日時を整形（例：2025-03-01 01時）
                time_label = f"{i+1:02d}:00"  # 時刻を整形（例：01:00）

                # 各項目を順に取得
                presipitation = "0.0" if cells[i * 16 + 2].text == "--" else cells[i * 16 + 2].text
                temp = cells[i * 16 + 3].text
                DewPoint = cells[i * 16 + 4].text
                steamPressure = cells[i * 16 + 5].text
                humidity = cells[i * 16 + 6].text
                windSpeed = cells[i * 16 + 7].text
                windDirection = cells[i * 16 + 8].text
                sunshine = "0.0" if cells[i * 16 + 9].text == "" else cells[i * 16 + 9].text
                globalRadiation = "0.0" if cells[i * 16 + 10].text == "" else cells[i * 16 + 10].text
                weather = cells[i * 16 + 13].find_element(By.TAG_NAME, "img").get_attribute("alt")
                visibility = cells[i * 16 + 15].text

                # 1時間分のデータをリストとしてまとめる
                data = [
                    date, time_label, presipitation, temp, DewPoint,
                    steamPressure, humidity, windSpeed, windDirection, sunshine,
                    globalRadiation, weather, visibility
                ]

                # データを画面に表示（確認用）
                #print(data)

                # CSV に書き込み
                writer.writerow(data)

    # 全てのループ終了後、ブラウザを閉じる
    driver.quit()

# -------------------------------
# 実行結果：Data/Environment.csv に、2025年3月〜11月の
# 日ごと・時間ごとの気象データが自動的に保存される。
# -------------------------------
