from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import re

chrome_driver_path = 'D:/Codes/chromedriver_win32'

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")

service = Service(chrome_driver_path)

with open("gameTime.csv", "w", encoding = "utf-8", newline = "") as file:
    writer = csv.writer(file)
    writer.writerow(["matchID,時間帯"])
    for i in range(4, 11):
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://npb.jp/bis/teams/calendar_c_" + f"{i:02d}" + ".html")

        driver.implicitly_wait(1)
        time.sleep(1)

        links = []

        # link = driver.find_element(By.XPATH, "//td[//div[contains(tevsteam)][//div]]]")
        linksParse = driver.find_elements(By.XPATH, "//a[contains(text(), '広') and contains(text(), '-')]")

        for i in linksParse:
            links.append(i.get_attribute("href"))

        # 試合
        for i in range(len(links)):
            driver.get(links[i])

            table = driver.find_elements(By.XPATH, "//table[.//tr[contains(@class, 'gmstats')]][contains(@class, 'gmtbltop')]")
            matchTitle = driver.find_elements(By.XPATH, "//h1")
            matchID = re.sub(r"[^0-9]+", "", matchTitle[1].text)
            matchDate = re.sub(r"[^0-9]+", "-", matchTitle[1].text)
            matchDate = matchDate.split("-")
            if (len(table) != 4):
                continue

            print(matchID)
            matchTime = driver.find_elements(By.XPATH, "//div[contains(@id, 'gmdivinfo')]")
            matchTime = matchTime[0].find_elements(By.XPATH, "//td[contains(@align, 'right')]")
            matchTimeString = matchTime[0].text.split(" ")
            matchTimeString = matchTimeString[3].split("　")
            print(matchTimeString[0][2:4], matchTimeString[1][2:4])

            writer.writerow([f"{matchID},{matchTimeString[0][2:4]} - {matchTimeString[1][2:4]}"])

        driver.quit()
        time.sleep(1)
