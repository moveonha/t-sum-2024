import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from sqlite3 import Error
import re


class IndexDB:

    db_name = "champions_index.sqlite"


    def __init__(self) -> None:
        pass


    @classmethod
    def create_champion_index_tables(cls):
        con = sqlite3.connect(cls.db_name)
        cur = con.cursor()

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS chamdex(
            champ_name TEXT NOT NULL UNIQUE,
            champ_index INTEGER NOT NULL UNIQUE
        )
        """
        )

    @classmethod
    def insert_champion_index(cls):
        con = sqlite3.connect(cls.db_name)
        cur = con.cursor()

        chamdex = ChampionIndex.make_chamdex_dict()

        for (name, index) in chamdex.items():
            cur.execute(
                f"INSERT INTO chamdex(champ_name, champ_index) VALUES ('{name}', {index});"
            )
        con.commit()
        con.close()


    @classmethod
    def drop_tables(cls):
        con = sqlite3.connect(cls.db_name)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS chamdex;")
        con.close()


    @staticmethod
    def make_index_table():
        IndexDB.drop_tables()
        IndexDB.create_champion_index_tables()
        IndexDB.insert_champion_index()



class ChampionIndex:
    
    champion_index = {}

    def __init__(self):
        pass


    @classmethod
    def make_chamdex_dict(cls):

        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        url = "https://fow.kr/statistics"
        driver.get(url)
        time.sleep(1)
        tbody_sel = driver.find_element(By.XPATH, '//*[@id="r_out"]')
        tbody = tbody_sel.get_attribute('innerHTML')
        driver.close()

        rows = tbody.split('</tr><tr>')
        
        i = 0
        for row in rows:
            cls.champion_index[row[row.find('"> ')+3:row.find("</td>")]] = i
            i += 1

        return cls.champion_index



class DataDB:

    db_name = 'game_results.sqlite'

    def __init__(self) -> None:
        pass

    @staticmethod
    def connection(db_name = "champions_index.sqlite"):
        con = sqlite3.connect(db_name)
        cursor_db = con.cursor()
        cursor_db.execute('SELECT * FROM chamdex')
        return cursor_db.fetchall()

    
    @classmethod
    def create_result_table(cls):
        con = sqlite3.connect(cls.db_name)
        cur = con.cursor()

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS games(
            train_champions TEXT NOT NULL,
            train_result INTEGER NOT NULL,
            test_champions TEXT,
            test_result INTEGER
        )
        """
        )

# ', '.join(s for s in str_list)

    @classmethod
    def insert_train_result(cls):
        con = sqlite3.connect(cls.db_name)
        cur = con.cursor()

        chams1 = DeepDatabase.deep_data[0][0]
        schams1 = []
        for i in chams1:
            schams1.append(', '.join(str(s) for s in i))

        chams2 = DeepDatabase.deep_data[1][0]
        schams2 = []
        for i in chams2:
            schams2.append(', '.join(str(s) for s in i))

        print(len(schams1), len(DeepDatabase.deep_data[0][1]), len(schams2), len(DeepDatabase.deep_data[1][1]))
        if len(schams1) != len(DeepDatabase.deep_data[0][1]) or len(schams2) != len(DeepDatabase.deep_data[1][1]):
            raise Exception("삐빅")

        for (champs1, result1, champs2, result2) in zip(schams1, DeepDatabase.deep_data[0][1], schams2, DeepDatabase.deep_data[1][1]):

            cur.execute(
                f"INSERT INTO games(train_champions, train_result, test_champions, test_result) VALUES ('{champs1}', {result1}, '{champs2}', {result2});"
            )
            # cur.execute(
            #     f"INSERT INTO games(test_champions, test_result) VALUES ('{champs2}', {result2});"
            # )
        con.commit()
        con.close()

    # @classmethod
    # def insert_test_result(cls):
    #     con = sqlite3.connect(cls.db_name)
    #     cur = con.cursor()

    #     chams2 = DeepDatabase.deep_data[1][0]
    #     schams2 = []
    #     for i in chams2:
    #         schams2.append(', '.join(str(s) for s in i))

    #     for (champs, result) in zip(schams2, DeepDatabase.deep_data[1][0]):
    #         cur.execute(
    #             f"INSERT INTO games(test_champions, test_result) VALUES ('{champs2}', {result2});"
    #         )
    #     con.commit()
    #     con.close()


    @classmethod
    def drop_tables(cls):
        con = sqlite3.connect(cls.db_name)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS games;")
        con.close()


    @staticmethod
    def make_result_table():
        DataDB.drop_tables()
        DataDB.create_result_table()
        DeepDatabase.make_train_data()
        DeepDatabase.make_test_data()
        DataDB.insert_train_result()
        # 
        # DataDB.insert_test_result()




class DeepDatabase:

    lankers = []

    train_data = []
    train_labels = []
    test_data = []
    test_labels = []

    deep_data = (train_data, train_labels), (test_data, test_labels)


    def __init__(self):
        pass

    @classmethod
    def make_lanker_list(cls, start_page, finish_page):
        cls.lankers = []
        for i in range(start_page, finish_page+1):                     # 몇 페이지 가져올건지
            driver = webdriver.Chrome()
            driver.implicitly_wait(5)
            url = "https://fow.kr/ranking#"+f"{i*50-49}"
            driver.get(url)
            tbody_sel = driver.find_element(By.XPATH, '//*[@id="r_out"]')
            tbody = tbody_sel.get_attribute('innerHTML')
            driver.close()
            for j in range(50):                    # 페이지당 몇 명 긁어올건지
                rows = tbody.split('</tr><tr>')
                cls.lankers.append(re.findall('">.+</a>', rows[j])[0][2:-4])
    
    @classmethod
    def make_train_data(cls, i):

        cls.make_lanker_list(i, i)    # 데이터 양 공식 : 30(인당 경기 수) * 50(페이지당 사람 수) * (finish_page - start_page)(페이지 수) 6000개

        for lanker in cls.lankers:
            driver = webdriver.Chrome()
            driver.implicitly_wait(5)
            url = "https://fow.kr/find/"+lanker
            driver.get(url)
            driver.find_element(By.PARTIAL_LINK_TEXT, "최근게임 더보기").click()
            time.sleep(1)
            table_sel = driver.find_element(By.CLASS_NAME, 'tablesorter.table_recent')
            table = table_sel.get_attribute('innerHTML')
            driver.close()
            tbody = table[table.find('tbody'):table.find('/tbody')]
            rows = tbody.split('</tr><tr>')

            for row in rows:
                temp_train_data = []
                temp_mine = row.split('</td><td')[1]
                a = DataDB.connection()
                champs = dict(a)
                temp_train_data.append(champs[temp_mine[temp_mine.find('<b>')+3:temp_mine.find('</b>')]])
                temp_team = row.split('</td><td')[6]
                for i in range(9):
                    temp_train_data.append(champs[temp_team[temp_team.find('alt="')+5:temp_team.find('" tipsy')]])
                    temp_team = temp_team[temp_team.find('" tipsy')+1:]
                cls.train_data.append(temp_train_data)

            DeepDatabase.make_train_labels(rows)




    
    @classmethod
    def make_train_labels(cls, rows):

            for row in rows:
                if row[row.find("</td>")-1] == '승':
                    cls.train_labels.append(1)
                elif row[row.find("</td>")-1] == '패':
                    cls.train_labels.append(0)
                else:
                    cls.train_labels.append(0)


    @classmethod
    def make_test_data(cls, i):

        cls.make_lanker_list(i, i)
        
        for lanker in cls.lankers:
            driver = webdriver.Chrome()
            driver.implicitly_wait(5)
            url = "https://fow.kr/find/"+lanker
            driver.get(url)
            driver.find_element(By.PARTIAL_LINK_TEXT, "최근게임 더보기").click()
            time.sleep(1)
            table_sel = driver.find_element(By.CLASS_NAME, 'tablesorter.table_recent')
            table = table_sel.get_attribute('innerHTML')
            driver.close()
            tbody = table[table.find('tbody'):table.find('/tbody')]
            rows = tbody.split('</tr><tr>')

            for row in rows:
                temp_test_data = []
                temp_mine = row.split('</td><td')[1]
                a = DataDB.connection()
                champs = dict(a)
                temp_test_data.append(champs[temp_mine[temp_mine.find('<b>')+3:temp_mine.find('</b>')]])
                temp_team = row.split('</td><td')[6]
                for i in range(9):
                    temp_test_data.append(champs[temp_team[temp_team.find('alt="')+5:temp_team.find('" tipsy')]])
                    temp_team = temp_team[temp_team.find('" tipsy')+1:]
                cls.test_data.append(temp_test_data)

            DeepDatabase.make_test_labels(rows)



    @classmethod
    def make_test_labels(cls, rows):

        # for lanker in cls.lankers:
        #     driver = webdriver.Chrome()
        #     driver.implicitly_wait(5)
        #     url = "https://fow.kr/find/"+lanker
        #     driver.get(url)
        #     driver.find_element(By.PARTIAL_LINK_TEXT, "최근게임 더보기").click()
        #     time.sleep(1)

        #     table_sel = driver.find_element(By.CLASS_NAME, 'tablesorter.table_recent')
        #     table = table_sel.get_attribute('innerHTML')
        #     driver.close()

        #     tbody = table[table.find('tbody'):table.find('/tbody')]
            
        #     rows = tbody.split('</tr><tr>')

            for row in rows:
                if row[row.find("</td>")-1] == '승':
                    cls.test_labels.append(1)
                elif row[row.find("</td>")-1] == '패':
                    cls.test_labels.append(0)
                else:
                    cls.test_labels.append(0)