import requests
from lxml import etree

def get_title(id):
    # URLを指定
    url = f'https://race.netkeiba.com/race/shutuba.html?race_id={id}'

    # requestsを使用してHTMLを取得
    response = requests.get(url)
    response.encoding = 'EUC-JP'
    html = response.text

    # lxmlを使用してHTMLをパース
    root = etree.HTML(html)

    title=''
    # XPathを使用して情報を抽出
    try:
        title = root.xpath('//*[@id="page"]/div[2]/div/div[1]/div[3]/div[2]/div[1]/span[1]/text')[0]
    except:
        title = root.xpath('//*[@id="page"]/div[2]/div/div[1]/div[3]/div[2]/div[1]')[0].text

    title  = title.replace('\n', '')
    return title