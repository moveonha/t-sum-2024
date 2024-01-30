import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import re




class ChampionIndex:

    champions_index_table = "champion_index.sqlite"
    def __init__(self):
        pass

    # 챔피언 인덱스 테이블 생성
    @classmethod
    def create_champion_index_tables(cls):
        con = sqlite3.connect(cls.champions_index_table)
        cur = con.cursor()

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS chamdex(
            champ_name TEXT NOT NULL UNIQUE,
            champ_index INTEGER NOT NULL UNIQUE
        )
        """
        )

    def insert_champion_index(cls):
        con = sqlite3.connect(cls.champions_index_table)
        cur = con.cursor()

        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        url = "https://fow.kr/statistics"

        driver.get(url)
        time.sleep(1)
        tbody_sel = driver.find_element(By.XPATH, '//*[@id="r_out"]')
        tbody = tbody_sel.get_attribute('innerHTML')
        driver.close()

        rows = tbody[4:-5].split('</tr><tr>')


        champion_index = {}
        i = 0

        for row in rows:
            
            champion_index[i] = row[row.find('"> ')+3:row.find("</td>")]
            i += 1
            cur.execute(
                f"INSERT INTO chamdex(champ_name, champion_index) VALUES ('{champion_index[i]}', {i});"
            )
        con.commit()
        con.close()
    




    @staticmethod
    def create_deeplearning_tables():
        con = sqlite3.connect(self.ch)
        con = sqlite3.connect('ch')
        cur = con.cursor()
        # menu table 생성
        cur.execute(
        )