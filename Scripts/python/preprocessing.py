import pandas as pd
import re
import datetime
import pickle
import glob
import os
import joblib
from sklearn.preprocessing import LabelEncoder

def get_practice(html_df):
    result = []
    html_df['調教タイム ラップ表示'] = html_df['調教タイム ラップ表示'].fillna('(0),(0),(0),(0),(0)')
    for s in html_df['調教タイム ラップ表示']:
        # 括弧で分割し、数値を取得
        numbers = []
        while True:
            try:
                if(len(numbers) == 5):
                    break
                if s[0] == '-':
                    numbers.append(0.0)
                    s = s[1:]
                    continue
                if s[0] in '中間':
                    numbers.append(0.0)
                    s = s[1:]
                    continue
                if s[0] in '連闘':
                    numbers.append(0.0)
                    s = s[1:]
                    continue
                if s[0] in '計時不能':
                    numbers.append(0.0)
                    s = s[1:]
                    continue
                for j in s.split(")"):
                    if(len(numbers) == 5):
                        break  
                    numbers.append(float(j.split('(')[0]))
                
            except Exception as e:
                break
            
        result.append(numbers)
    practice = pd.DataFrame(columns=['5C', '4C', '3C', '2C', '1C'])
    for i in result:
        if len(i) != 5:
            i.append(0.0)
        new_row = pd.DataFrame([{'1C': str(i[0]), '2C': str(i[1]), '3C': str(i[2]), '4C': str(i[3]), '5C': str(i[4])}])
        practice = pd.concat([practice, new_row], ignore_index=True)
    return pd.concat([html_df, practice], axis=1)[['馬 番', 'コース', '馬場', '脚色', '5C', '4C', '3C', '2C', '1C']]



def prepro_race_name(df, title):
    def setRace(race):
        if 'G1' in race:
            return 'G1'
        elif 'G2' in race:
            return 'G2'
        elif 'G3' in race:
            return 'G3'
        elif 'OP' in race:
            return 'OP'
        elif '(L)' in race:
            return 'L'
        elif '1勝クラス' in race:
            return '1勝クラス'
        elif '3勝クラス' in race:
            return '3勝クラス'
        elif '2勝クラス' in race:
            return '2勝クラス'
        elif '1600万下' in race:
            return 'その他'
        elif '1000万下' in race:
            return 'その他'
        elif '500万下' in race:
            return 'その他'
        elif '葵S(G)' in race:
            return 'その他'

        return race
    df['レース名'] = title
    df['レース名'] = df['レース名'].apply(setRace)
    return df


def change_tyoukyou_race_name(df):
    df = df.rename({'コース' : '調教コース'}, axis=1)
    df['調教コース'].replace('栗坂', '栗東', inplace=True)
    df['調教コース'].replace('南Ｗ', '三浦', inplace=True)
    df['調教コース'].replace('南Ｄ', '三浦', inplace=True)
    df['調教コース'].replace('ＣＷ', '栗東', inplace=True)
    df['調教コース'].replace('函Ｗ', '函館', inplace=True)
    df['調教コース'].replace('札ダ', '札幌', inplace=True)
    df['調教コース'].replace('美Ｐ', '三浦', inplace=True)
    df['調教コース'].replace('美坂', '三浦', inplace=True)
    df['調教コース'].replace('小ダ', '小倉', inplace=True)
    df['調教コース'].replace('北Ｃ', '三浦', inplace=True)
    df['調教コース'].replace('ＤＰ', '栗東', inplace=True)
    df['調教コース'].replace('栗Ｂ', '栗東', inplace=True)
    df['調教コース'].replace('栗芝', '栗東', inplace=True)
    df['調教コース'].replace('栗飛', '栗東', inplace=True)
    df['調教コース'].replace('札芝', '札幌', inplace=True)
    df['調教コース'].replace('函ダ', '函館', inplace=True)
    df['調教コース'].replace('南芝', '三浦', inplace=True)
    df['調教コース'].replace('函芝', '函館', inplace=True)
    df['調教コース'].replace('南ダ', '三浦', inplace=True)
    df['調教コース'].replace('栗Ｅ', '栗東', inplace=True)
    df['調教コース'].replace('門坂', '札幌', inplace=True)
    df['調教コース'].replace('小障', '小倉', inplace=True)
    df['調教コース'].replace('小芝', '小倉', inplace=True)
    df['調教コース'].replace('栗障', '栗東', inplace=True)
    df['調教コース'].replace('北Ｂ', '三浦', inplace=True)
    df['調教コース'].replace('船橋', '三浦', inplace=True)
    df['調教コース'].replace('新ダ', '三浦', inplace=True)
    df['調教コース'].replace('美Ｗ', '三浦', inplace=True)
    df['調教コース'].replace('美ダ', '三浦', inplace=True)
    df['調教コース'].replace('美芝', '三浦', inplace=True)
    mode = df['調教コース'].mode()[0]
    df['調教コース'].fillna(mode, inplace=True)
    return df


def all_preprocessing(df, result, main):
    df['輸送時間'] = result
    df = df[~df['馬体重 (増減)'].str.contains('--')]
    df = df.assign(体重 = lambda x: (x['馬体重 (増減)'].str[:3]))
    df = df.assign(増減=lambda x: x['馬体重 (増減)'].str[4].apply(lambda s: 'プラス' if s == '+' else 'マイナス' if s == '-' else '変化なし'))
    df.loc[df['馬体重 (増減)'].str.contains('前計不'), '馬体重 (増減)'] = '00000'
    pattern = r"\d+"
    df = df.assign(増減値=lambda x: x['馬体重 (増減)'].str[4:].apply(lambda s: re.findall(pattern, s)[0]))
    df = df.drop('馬体重 (増減)', axis=1)

    df = df.rename(columns={'馬場': '調教馬場'})
    df = df.drop('人気', axis=1)

    df = df.assign(年齢 = lambda x: (x['性齢'].str[-1]))
    df['歳'] = df['年齢'].astype(int)
    pattern = r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]+'
    df['性別'] = df['性齢'].apply(lambda x : re.findall(pattern, x)[0])
    df = df.drop('性齢', axis=1)
    df['頭数'] = len(df)

    df = df.rename({'id': 'jockey_id', 'index': 'horse_id'}, axis=1)

    dt_now = datetime.datetime.now().month
    def date_change(tmp):
        if tmp < 4:
            return 0
        elif 4 <= tmp < 7:
            return 1
        elif 7 <= tmp < 10:
            return 2
        return 3

    df['日付'] = date_change(dt_now)
    df = df.rename({'本馬場':'situation', '天気': 'whether', '形態' : 'track'}, axis=1)
    df['rightORleft'] = df['rightORleft'].apply(lambda x : '右' if '右' in x else '左')

    for x in glob.glob('D:/03_keiba/Scripts/python/label_encoder/*'):
        file_name = os.path.splitext(os.path.basename(x))[0]
        if file_name in df.columns:
            encoder = joblib.load(x)
            try:
                df[file_name] = encoder.transform(df[file_name])
            except:
                continue
    if len(main) == len(df):
        main = main.assign(horse_deokure_avg = lambda x : x['deokureNum'] / x['raceNum'])
        df = df.merge(main, left_on='horse_id', right_on='index')
        df = df.drop(['deokureNum', 'raceNum'], axis=1)
    else:
        df['horse_deokure_avg'] = 0

    j_df = joblib.load('D:/03_keiba/Scripts/pkl/jockey_avg.pickle')
    def get_jockey_avg(j_id):
        if len(j_id) == 4:
            j_id = '0' + j_id
        elif len(j_id) == 6:
            j_id = j_id[0:4]
        try:
            return_id = j_df.loc[j_df.jockey_id == j_id, 'target'].iloc[0]
            return return_id
        except:
            return 0
    df['jockey_deokure_avg'] = df['jockey_id'].apply(get_jockey_avg)
    df = df.rename({'枠' : '枠番', '馬 番': '馬番'}, axis=1)
    df = df[['枠番', '馬番', '斤量', '調教師', 'track', 'rightORleft', 'whether', 'situation', '体重', '増減', '距離', '調教コース', '調教馬場', '脚色', '1C', '2C', '3C', '4C', '5C', '日付', '開催', 'レース名', '頭数', '開催数', '開催日付', '増減値', '歳', '性別', 'jockey_deokure_avg', 'horse_deokure_avg', '輸送時間']]
    return df