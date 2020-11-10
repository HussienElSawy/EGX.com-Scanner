import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd 
import time



def generate_table(soup,id,table_name,type,timestamp):
    table = soup.find('table',id=id)
    row_1= table.find_all('tr')[1]
    columns = len(row_1.find_all('td'))
    df = pd.DataFrame(columns=range(0,columns+1), index=[0])
    new_table = pd.DataFrame(columns=range(0,columns+1), index=[0]) 
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            new_table.iat[row_marker,column_marker] = column.get_text()
            column_marker += 1
        new_table.iat[row_marker,column_marker] = timestamp
        df = df.append(new_table)
    
    if os.path.exists("outputs/"+type+"/"+table_name+".csv"):
        df.to_csv("outputs/"+type+"/"+table_name+".csv",mode='a', index=False, header=False)
    else:
        df.to_csv("outputs/"+type+"/"+table_name+".csv", index=False)

# check if all needed folders exists
if not os.path.exists("outputs"):
    os.mkdir("outputs")
    
if not os.path.exists("outputs/All"):
    os.mkdir("outputs/All")
    
if not os.path.exists("outputs/Bonds"):
    os.mkdir("outputs/Bonds")
    
if not os.path.exists("outputs/Securities"):
    os.mkdir("outputs/Securities")
    
# URL to read data from
URL = "https://www.egx.com.eg/en/investorstypepiechart.aspx"

# Form-Data parameters
"""
to choose All (Securties + Bonds) use the following values 
types = All
events = ctl00$C$rblSecuritiesBonds$0

to choose Securties only use the following values 
types = Securities
events = ctl00$C$rblSecuritiesBonds$1

to choose Securties only use the following values 
types = Bonds
events = ctl00$C$rblSecuritiesBonds$2
"""

while True:
    now = datetime.now()
    for i in range(3):
        print(i)
        if i == 0:
            type = 'All'
            event = "ctl00$C$rblSecuritiesBonds$0"
        elif i == 1:
            type = 'Securities'
            event = "ctl00$C$rblSecuritiesBonds$1"
        elif i == 2:
            type = 'Bonds'
            event = "ctl00$C$rblSecuritiesBonds$2"
        PARAMS = {"__EVENTTARGET": event, "__VIEWSTATE": "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","__VIEWSTATEGENERATOR": "F88730C4","ctl00$H$rblSearchType": "1","ctl00$C$rblSecuritiesBonds": type} 
        timestamp = now.strftime('%d/%m/%y.%H:%M')
        webpage_url = requests.post(url = URL, data = PARAMS)
        soup = BeautifulSoup(webpage_url.text, 'lxml')
        generate_table(soup,'ctl00_C_Pc_GridView1','Total',type,timestamp)
        generate_table(soup,'ctl00_C_Pc_gvInstByNationality','InstitutionsbyNationality',type,timestamp)
        generate_table(soup,'ctl00_C_Pc_gvIndByNationality','IndividualsbyNationality',type,timestamp)
    time.sleep(55)