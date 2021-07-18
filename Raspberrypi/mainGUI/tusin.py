import json
import requests
import csv
import pandas as pd # py -m pip install pandas
import os
from requests import exceptions
from requests.exceptions import Timeout




# 多分動く getのみのスクリプトは動いてた
def get_risyudata(kamoku): # kamokuは科目IDでstr型
    dir_path = "../data/input"
    os.makedirs(dir_path, exist_ok=True)
    get_url = "http//localhost:5000/csv/?kamoku="+kamoku
    try:
        url = requests.get(get_url)
        text = url.text
        data = json.loads(text)
        print(data)
        #fileName = 'syusseki_data.json'
        #file = open(fileName,"w")
        #json.dump(data, file)
        # file.close()
        #print(data)

        df_json = pd.DataFrame(data["csv"])
        df_json = df_json.T
        # print(df_json)
        out_risyu = dir_path + "/risyu_" + kamoku + ".csv"
        df_json.to_csv(out_risyu, encoding='utf-8',index=False)
        # print(type(df_json))

        df_json = pd.DataFrame(data['kisoku'])
        df_json = df_json.T
        out_kisoku = dir_path + "/kisoku_" + kamoku + ".csv" 
        df_json.to_csv(out_kisoku, encoding='utf-8')
        print("ダウンロード・ファイル保存完了")
        return True
    except:
        return False




# データ1パターンは動いた
# 謎だけど動く(はず)
def post(kaisu,kamoku): # kaisuはint型 kamokuは科目IDでstr型
    open_name = "data/output/" + kamoku + "_" + str(kaisu) + ".csv"
    df_names = pd.read_csv(open_name, names=('number', 'name', 'n', 's','id','syusseki'))
    df_names = df_names.drop(columns=['name','n','s','id'])
    csv_read = df_names.to_dict(orient="index")
    data = []
    for n in range(len(csv_read)):
        data.append(csv_read[n])
    
    jdata = {}
    jdata["kaisu"] = kaisu
    jdata["kamoku"] = kamoku
    jdata["csv"] = data
    print(jdata)
    try:
        response = requests.post(
        'http://127.0.0.1:5000/csv/',
            json=json.dumps(jdata))#,
            #headers={'Content-Type': 'application/json'})
        # pprint.pprint(response.json())
        #resDatas = response.json()
        return True
    except:
        return False