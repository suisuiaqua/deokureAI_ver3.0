from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from time import sleep
import pandas as pd
from tqdm import tqdm
import warnings
warnings.simplefilter('ignore')

def mainScrape(df):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')             
    options.add_argument('--disable-extensions')       
    options.add_argument('--proxy-server="direct://"') 
    options.add_argument('--proxy-bypass-list=*')      
    options.add_argument('--start-maximized')  
    service = Service(executable_path="")
    driver = webdriver.Chrome(service=service, options=options)
    horse_id_list = df['horse_id']
    target_url = "https://regist.netkeiba.com/account/?pid=login"
    driver.get(target_url)
    sleep(1)

    USERNAME = ""
    PASSWORD = ""

    username_input = driver.find_elements(By.XPATH,'//*[@id="contents"]/div/form/div/ul/li[1]/input')
    username_input[0].send_keys(USERNAME)
    sleep(1)

    username_input = driver.find_elements(By.XPATH,'//*[@id="contents"]/div/form/div/ul/li[2]/input')
    username_input[0].send_keys(PASSWORD)
    sleep(1)

    username_input = driver.find_elements(By.XPATH,'//*[@id="contents"]/div/form/div/div[1]/input')
    username_input[0].click()
    sleep(1)

    deokure_count_detail = {}
    for horse_id in tqdm(horse_id_list):
        try:
            sleep(1)
            rece = driver.get('https://db.netkeiba.com/horse/' + horse_id)
            sleep(1)
            table = driver.find_elements(By.XPATH,'//*[@id="contents"]/div[4]/div/table')
            html = table[0].get_attribute('outerHTML')

            deokureCount = 0
            for i in range(len(pd.read_html(html)[0])):
                if '出遅れ' == pd.read_html(html)[0].loc[[i]]['備考'][i]:
                    deokureCount = deokureCount + 1

            horse_detail_list = []
            horse_detail = []
            horse_detail.append(deokureCount)
            horse_detail.append(len(pd.read_html(html)[0]))
            horse_detail_list.append(horse_detail)
            deokure_count_detail[horse_id] = pd.DataFrame(horse_detail_list,columns=['deokureNum','raceNum'])
        except Exception:
            continue

    for key in deokure_count_detail:
        deokure_count_detail[key].index = [key] * len(deokure_count_detail[key])
    results = pd.concat([deokure_count_detail[key] for key in deokure_count_detail], sort=False)
    results = results.reset_index()
    driver.quit()
    return results
    