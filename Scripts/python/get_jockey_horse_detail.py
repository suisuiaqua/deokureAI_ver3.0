from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from time import sleep
import pandas as pd
import re
from tqdm import tqdm
import warnings
warnings.simplefilter('ignore')


def raceScrape_jockeyID_horseID(id):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')             
    options.add_argument('--disable-extensions')       
    options.add_argument('--proxy-server="direct://"') 
    options.add_argument('--proxy-bypass-list=*')      
    options.add_argument('--start-maximized')  
    service = Service(executable_path="D:/chromedriver_win32/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    url = f'https://race.netkeiba.com/race/shutuba.html?race_id={id}'
    df = pd.read_html(url, encoding='EUC-JP')[0]

    # カラムが二重なので取り除く
    newCol = []
    for i in df.columns:
        newCol.append(i[0])
    df.columns = newCol


    target_url = url
    driver.get(target_url)
    sleep(1)

    table = driver.find_elements(By.XPATH,'//*[@id="page"]/div[3]/div[2]/table/tbody/tr')
    horse_jockey_id = []
    for i in tqdm(range(1,len(table)+1)):
        result_id = []

        # horse_id
        sleep(1)
        horse_id = driver.find_elements(By.XPATH,'//*[@id="page"]/div[3]/div[2]/table/tbody/tr[' + str(i) +']/td[4]')
        horse_id = re.sub( r'\D+', '', horse_id[0].get_attribute('outerHTML').split('/horse')[1].split('title')[0])
        result_id.append(horse_id)

        # jockey_id
        sleep(1)
        jockey_id = driver.find_elements(By.XPATH,'//*[@id="page"]/div[3]/div[2]/table/tbody/tr[' + str(i) +']/td[7]')
        jockey_id = re.sub( r'\D+', '', jockey_id[0].get_attribute('outerHTML').split('/recent')[1])
        result_id.append(jockey_id)

        horse_jockey_id.append(result_id)  

    df = pd.concat([df, pd.DataFrame(horse_jockey_id,columns=['horse_id', 'jockey_id'])], axis=1)
    driver.quit()
    return df