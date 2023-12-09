import requests
from lxml import etree
import re


def get_detail_df(df, id):
    # URLを指定
    url = 'https://race.netkeiba.com/race/result.html?race_id=' + id
    response = requests.get(url)
    html = response.content
    root = etree.HTML(html)

    baba = root.xpath('//*[@id="page"]/div[2]/div/div[1]/div[3]/div[2]/div[2]/span[3]')[0]
    df['本馬場'] = baba.text.split(':')[1]

    distance = root.xpath('//*[@id="page"]/div[2]/div/div[1]/div[3]/div[2]/div[2]/span[1]')[0]
    df['形態'] = distance.text[1]

    distance = root.xpath('//*[@id="page"]/div[2]/div/div[1]/div[3]/div[2]/div[2]/span[1]')[0]
    df['距離'] = int(re.findall(r'\d+', distance.text)[0])

    rightORleft = root.xpath('//*[@id="page"]/div[2]/div/div[1]/div[3]/div[2]/div[2]/text()[2]')[0]
    rightORleft = re.findall( r'\((.*?)\)', rightORleft)[0]
    df['rightORleft'] = rightORleft

    weather = root.xpath('//*[@id="page"]/div[2]/div/div[1]/div[3]/div[2]/div[2]/text()[2]')[0]
    df['天気'] = weather[-1]

    url = 'https://race.netkeiba.com/race/result.html?race_id=' + id
    response = requests.get(url)
    html = response.content
    root = etree.HTML(html)

    kaisai_num = root.xpath('//*[@id="page"]/div[2]/div/div[1]/div[3]/div[2]/div[3]/span[1]')[0].text
    df['開催数'] = re.findall('\S', kaisai_num)[0]

    kaisai = root.xpath('//*[@id="page"]/div[2]/div/div[1]/div[3]/div[2]/div[3]/span[2]')[0].text
    df['開催'] = kaisai

    kaisai_num = root.xpath('//*[@id="page"]/div[2]/div/div[1]/div[3]/div[2]/div[3]/span[3]')[0].text
    df['開催日付'] = re.findall('\S', kaisai_num)[0]

    return df