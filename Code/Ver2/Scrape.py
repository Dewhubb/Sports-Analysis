# アントニ担当: 10チームの試合データと各試合の気象データのデータ収集    

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import re
import pandas as pd

chrome_driver_path = 'D:/Codes/chromedriver_win32'

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")

service = Service(chrome_driver_path)

name = []
swing = []
hit = []
score = []

teamCodes = {"Hiroshima": ["c", "広島東洋", "広"],
             "Hokkaido": ["f", "日本ハム", "日"],
             "Yomiuri": ["g", "読　売", "巨"],
             "Hanshin": ["t", "阪　神", "神"],
             "Fukuoka": ["h", "福岡ソフトバンク", "ソ"],
             "DeNA": ["db", "横浜DeNA", "デ"],
             "Yakult": ["s", "東京ヤクルト", "ヤ"],
             "Chiba": ["m", "千葉ロッテ", "ロ"],
             "Rakuten": ["t", "東北楽天", "楽"],
             "Saitama": ["l", "埼玉西武", "西"]}

stadiumList = pd.read_csv("stadiumList.csv")

driver = webdriver.Chrome(options=chrome_options)

for teamName, teamCode in teamCodes.items():
    with open(f"game{teamName}.csv", "w", encoding = "utf-8", newline = "") as file:
        with open(f"gameTime{teamName}.csv", "w", encoding = "utf-8", newline = "") as file2:
            with open(f"gameStadium{teamName}.csv", "w", encoding = "utf-8", newline = "") as file3:
                with open(f"environment{teamName}.csv", "w", encoding = "utf-8", newline = "") as file4:
                    writer = csv.writer(file, quoting = csv.QUOTE_NONE, delimiter='\t')
                    writer2 = csv.writer(file2, quoting = csv.QUOTE_NONE, delimiter='\t')
                    writer3 = csv.writer(file3, quoting = csv.QUOTE_NONE, delimiter='\t')
                    writer4 = csv.writer(file4, quoting = csv.QUOTE_NONE, delimiter='\t')
                    writer.writerow(["matchID,名前,打数,安打,打率,打点"])
                    writer2.writerow(["matchID,開始時間,終了時間"])
                    writer3.writerow(["matchID,球場"])
                    writer4.writerow(["日付,時刻,降水量(mm),気温(°C),露点温度(°C),蒸気圧(hPa),湿度(%),風速(m/s),風向,日照時間(h),全天日射量(MJ/㎡),天気,視程(km)"])
                    
                    for i in range(4, 11):
                        driver.get(f"https://npb.jp/bis/teams/calendar_{teamCode[0]}_" + f"{i:02d}" + ".html")

                        driver.implicitly_wait(1)
                        time.sleep(3)

                        links = []

                        # link = driver.find_element(By.XPATH, "//td[//div[contains(tevsteam)][//div]]]")
                        linksParse = driver.find_elements(By.XPATH, f"//a[contains(text(), '{teamCode[2]}') and contains(text(), '-')]")

                        for j in linksParse:
                            links.append(j.get_attribute("href"))

                        # 試合
                        for j in range(len(links)):
                            driver.get(links[j])

                            table = driver.find_elements(By.XPATH, "//table[.//tr[contains(@class, 'gmstats')]][contains(@class, 'gmtbltop')]")
                            team = driver.find_elements(By.XPATH, "//table[.//tbody[.//tr[.//td[.//table[.//tbody[.//tr[.//td[contains(@class, 'flagteam2')]]]]]]]]")
                            matchTitle = driver.find_elements(By.XPATH, "//h1")
                            matchID = re.sub(r"[^0-9]+", "", matchTitle[1].text)
                            matchDate = re.sub(r"[^0-9]+", "-", matchTitle[1].text)
                            matchDate = matchDate.split("-")
                            month = int(matchDate[1])
                            day = int(matchDate[2])

                            print(matchID)

                            if (len(table) != 4):
                                continue
                            
                            # 時間
                            matchInfo = driver.find_elements(By.XPATH, "//div[contains(@id, 'gmdivinfo')]")
                            matchInfo = matchInfo[0].find_elements(By.XPATH, ".//td")
                            matchStadium = matchInfo[0].text
                            matchTimeString = matchInfo[1].text.split(" ")
                            matchTimeString = matchTimeString[3].split("　")
                            writer2.writerow([f"{matchID},{matchTimeString[0][2:4]},{matchTimeString[1][2:4]}"])

                            writer3.writerow([f"{matchID},{matchStadium}"])

                            if (teamCode[1] in team[1].text):
                                teamIndex = 0
                            else:
                                teamIndex = 1

                            for k in range(1, 3):
                                print(team[k].text)

                            data = table[teamIndex].text[24:].split("\n")

                            for k in range(len(data)):
                                line = data[k].split(" ")
                                lineName = line[1]
                                
                                if (lineName not in name):
                                    name.append(lineName)
                                    swing.append(0)
                                    hit.append(0)
                                    score.append(0)
                                    nameIndex = len(name) - 1

                                else:
                                    nameIndex = name.index(lineName)
                                
                                swing[nameIndex] += int(line[2])
                                hit[nameIndex] += int(line[3])
                                score[nameIndex] += int(line[4])

                                rate = 0

                                if int(line[2]) != 0:
                                    rate = int(line[3]) / int(line[2])

                                writer.writerow([f"{matchID},{lineName},{line[2]},{line[3]},{rate},{line[4]}"])

                                print(str(k) + ": " + data[k])

                            # 気象
                            # 気象データは野球場に基づいて収集されるため、一回目の実行では収集しない。

                            for row in stadiumList.itertuples():
                                if (row[1] == matchStadium):
                                    stadiumIDprec = row[2]
                                    stadiumIDblock = row[3]

                            url = f"https://www.data.jma.go.jp/stats/etrn/view/hourly_s1.php?prec_no={stadiumIDprec}&block_no={stadiumIDblock}&year=2025&month={month:02d}&day={day:02d}&view="
                            driver.get(url)

                            cells = driver.find_elements(By.XPATH, "//td[contains(@class, 'data_0_0')]")

                            # ディウ担当
                            for i in range(int(len(cells) / 16)):  # 1行あたり16列のデータがある
                                date = f"2025{matchDate[1]}{matchDate[2]}"  # 日時を整形（例：2025-03-01 01時）
                                time_label = f"{i+1:02d}:00"  # 時刻を整形（例：01:00）

                                # 各項目を順に取得
                                presipitation = "0.0" if cells[i * 16 + 2].text == "--" else cells[i * 16 + 2].text
                                temp = cells[i * 16 + 3].text
                                dewPoint = cells[i * 16 + 4].text
                                steamPressure = cells[i * 16 + 5].text
                                humidity = cells[i * 16 + 6].text
                                windSpeed = cells[i * 16 + 7].text
                                windDirection = cells[i * 16 + 8].text
                                sunshine = "0.0" if cells[i * 16 + 9].text == "" else cells[i * 16 + 9].text
                                globalRadiation = "0.0" if cells[i * 16 + 10].text == "" else cells[i * 16 + 10].text
                                try:
                                    driver.implicitly_wait(0.1)
                                    weather = cells[i * 16 + 13].find_element(By.TAG_NAME, "img").get_attribute("alt")
                                except:
                                    weather = ""
                                driver.implicitly_wait(1)
                                visibility = cells[i * 16 + 15].text

                                # CSV に書き込み
                                writer4.writerow([f"{date},{time_label},{presipitation},{temp},{dewPoint},{steamPressure},{humidity},{windSpeed},{windDirection},{sunshine},{globalRadiation},{weather},{visibility}"])

driver.quit()