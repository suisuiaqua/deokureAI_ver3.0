from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from time import sleep
from bs4 import BeautifulSoup
import requests
from lxml import etree
import pandas as pd

def get_html_df(id):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')             
    options.add_argument('--disable-extensions')       
    options.add_argument('--proxy-server="direct://"') 
    options.add_argument('--proxy-bypass-list=*')      
    options.add_argument('--start-maximized')  
    service = Service(executable_path="D:/chromedriver_win32/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    target_url = "https://regist.netkeiba.com/account/?pid=login"
    driver.get(target_url)
    sleep(1)

    USERNAME = "iijima.suisuiaqua1101@gmail.com"
    PASSWORD = "sakadonishi15"

    username_input = driver.find_elements(By.XPATH,'//*[@id="contents"]/div/form/div/ul/li[1]/input')
    sleep(1)
    username_input[0].send_keys(USERNAME)
    sleep(1)

    username_input = driver.find_elements(By.XPATH,'//*[@id="contents"]/div/form/div/ul/li[2]/input')
    username_input[0].send_keys(PASSWORD)
    sleep(1)

    username_input = driver.find_elements(By.XPATH,'//*[@id="contents"]/div/form/div/div[1]/input')
    sleep(1)
    username_input[0].click()
    sleep(1)
    url = f'https://race.netkeiba.com/race/oikiri.html?race_id={id}'
    driver.get(url)
    sleep(1)
    table = driver.find_elements(By.TAG_NAME,'table')
    html_df = pd.read_html(table[0].get_attribute('outerHTML'))[0]
    return html_df




def tyoukyoushi(df, tyoukyoushi_list):
    def getTyoukyoushi(horse_id):
        sleep(1)
        url = f'https://db.netkeiba.com/horse/{horse_id}'
        response = requests.get(url)
        html = response.content
        root = etree.HTML(html)
        soup = BeautifulSoup(html, 'html.parser')

        tyoukyousi = soup.select_one('#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > table > tr:nth-child(2)').text.strip().split('\n')[1].split('(')[0].strip()

        if any(element in tyoukyousi for element in tyoukyoushi_list):
            return tyoukyousi
        return '名もなき調教師'

    df.loc[:, '調教師'] = df['horse_id'].apply(getTyoukyoushi)
    return df