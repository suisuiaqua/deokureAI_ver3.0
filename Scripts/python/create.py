import pandas as pd;

def create_shipping_time(df):
    result = []
    print('実行')
    for co, kai in zip(df['調教コース'], df['開催']):
        if (co == '栗東'):
            if (kai == '京都'):
                result.append(0)
            elif (kai == '阪神'):
                result.append(2)
            elif (kai == '中京'):
                result.append(3)
            elif (kai == '東京'):
                result.append(10)
            elif (kai == '中山'):
                result.append(6)
            elif (kai == '小倉'):
                result.append(6)
            elif (kai == '福島'):
                result.append(8)
            elif (kai == '札幌'):
                result.append(15)
            elif (kai == '函館'):
                result.append(20)
            elif (kai == '新潟'):
                result.append(6)
                
        if (co == '三浦'):
            if (kai == '京都'):
                result.append(7)
            elif (kai == '阪神'):
                result.append(8)
            elif (kai == '中京'):
                result.append(6)
            elif (kai == '東京'):
                result.append(2)
            elif (kai == '中山'):
                result.append(2)
            elif (kai == '小倉'):
                result.append(13)
            elif (kai == '福島'):
                result.append(3)
            elif (kai == '札幌'):
                result.append(10)
            elif (kai == '函館'):
                result.append(15)
            elif (kai == '新潟'):
                result.append(4)

        if (co == '函館'):
            if (kai == '京都'):
                result.append(15)
            elif (kai == '阪神'):
                result.append(15)
            elif (kai == '中京'):
                result.append(15)
            elif (kai == '東京'):
                result.append(15)
            elif (kai == '中山'):
                result.append(15)
            elif (kai == '小倉'):
                result.append(15)
            elif (kai == '福島'):
                result.append(15)
            elif (kai == '札幌'):
                result.append(4)
            elif (kai == '函館'):
                result.append(0)
            elif (kai == '新潟'):
                result.append(20)

        if (co == '札幌'):
            if (kai == '京都'):
                result.append(15)
            elif (kai == '阪神'):
                result.append(15)
            elif (kai == '中京'):
                result.append(15)
            elif (kai == '東京'):
                result.append(15)
            elif (kai == '中山'):
                result.append(15)
            elif (kai == '小倉'):
                result.append(15)
            elif (kai == '福島'):
                result.append(15)
            elif (kai == '札幌'):
                result.append(0)
            elif (kai == '函館'):
                result.append(4)
            elif (kai == '新潟'):
                result.append(20)


        if (co == '小倉'):
            if (kai == '京都'):
                result.append(6)
            elif (kai == '阪神'):
                result.append(6)
            elif (kai == '中京'):
                result.append(10)
            elif (kai == '東京'):
                result.append(15)
            elif (kai == '中山'):
                result.append(15)
            elif (kai == '小倉'):
                result.append(0)
            elif (kai == '福島'):
                result.append(10)
            elif (kai == '札幌'):
                result.append(20)
            elif (kai == '函館'):
                result.append(20)
            elif (kai == '新潟'):
                result.append(20)
        if (co == '調教なし'):
            result.append(9999)
            
    return result