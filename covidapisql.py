import requests
import json
import os
import sqlite3

def getCovidData():
    try:
        resp=requests.get('https://api.covid19api.com/summary')
        data=json.loads(resp.text)
    except:
        print("Could not get API data")
    country=data["Countries"]
    covidlist=[]
    for x in country:
        tup=(x["Country"],x["TotalConfirmed"],x["TotalDeaths"])
        covidlist.append(tup)
    return covidlist

def createDB(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
        
    cur.execute('CREATE TABLE IF NOT EXISTS APIdata (Country TEXT, TotalCases INTEGER, TotalDeaths INTEGER)')
    conn.commit()
    return cur, conn



def addData(db_name, data, cur, conn):
    for tup in data:
        try:
            country = tup[0]
            TotalCases = tup[1]
            TotalDeaths=tup[2]
        except:
            country_id = 0
            TotalCases = 0
            TotalDeaths=0
        cur.execute('INSERT OR IGNORE INTO  APIData (Country, TotalCases, TotalDeaths) VALUES (?, ?, ?)', (country, TotalCases,TotalDeaths))
            
    conn.commit()

def main():
    db_name = "APIDataStored"
    data=getCovidData()
    c, d = createDB(db_name)
    addData(db_name, data, c, d)

main()