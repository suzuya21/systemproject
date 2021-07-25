"""
ラズパイとの通信部分
http://serverIP/csv
"""
import json
import requests
import csv
import pandas as pd # py -m pip install pandas
import os
from requests import exceptions
from requests.exceptions import Timeout
from GenerateInformation import generate


serverIP = "192.168.1.17"
port = '13431'
# 多分動く getのみのスクリプトは動いてた
def get_risyudata(kamoku): # kamokuは科目IDでstr型
    datapath = os.path.join(os.path.dirname(os.path.dirname(__file__)),f'data/')
    dir_path = os.path.join(datapath,"input")
    output_dir_path = os.path.join(datapath,"output") # おまけでoutputもつくっておく
    os.makedirs(dir_path, exist_ok=True)
    os.makedirs(output_dir_path, exist_ok=True)
    get_url = 'http://' + serverIP + ':' + port +"/csv/?kamoku="+kamoku
    try:
        url = requests.get(get_url,timeout=3.0)
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
        generate(kamoku, os.path.abspath(os.path.join(dir_path,f'kisoku_{kamoku}.csv')), os.path.abspath(os.path.join(dir_path,f'risyu_{kamoku}.csv')))
        return True
    except:
        import traceback
        traceback.print_exc()
        return False




# データ1パターンは動いた
# 謎だけど動く(はず)
def post(kaisu,kamoku): # kaisuはint型 kamokuは科目IDでstr型
    try:
        datapath = os.path.join(os.path.dirname(os.path.dirname(__file__)),f'data/')
        open_name = os.path.join(datapath,"output/" + kamoku + "_" + str(kaisu) + ".csv")
        df_names = pd.read_csv(open_name, names=('id', 'name', 'number','syusseki'))
        df_names = df_names.drop(columns=['id','name'])
        csv_read = df_names.to_dict(orient="index")
        data = []
        for n in range(len(csv_read)):
            data.append(csv_read[n])

        jdata = {}
        jdata["kaisu"] = kaisu
        jdata["kamoku"] = kamoku
        jdata["csv"] = data
        print(jdata)
    except:
        import traceback
        traceback.print_exc()
        return False
    try:
        response = requests.post(
            'http://' + serverIP + ':' + port + '/csv/',
            json=json.dumps(jdata),timeout=3.0)#,
            #headers={'Content-Type': 'application/json'})
        # pprint.pprint(response.json())
        #resDatas = response.json()
        print('response:',response.status_code)
        if response.status_code == 200:
            os.remove(open_name)
            return True
        return False
    except:
        import traceback
        traceback.print_exc()
        return False
