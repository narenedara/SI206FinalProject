import requests
import json
from bs4 import BeautifulSoup
import os
import sqlite3


def getObesityData():
    url = "https://en.m.wikipedia.org/wiki/List_of_sovereign_states_by_obesity_rate"
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        data = []
        obesitylist=[]

        table = soup.find_all('td')
        table2= soup.find_all('tr')
    except:
        print("Didnt work")



    for item in table:
        deez=soup.find_all('a')
        for x in deez:
            if (x.text) not in data:
                data.append(x.text)
    realcountry=data[19:210]


    for x in table2:
        td=soup.find_all('td')
        for x in td:
            if "." in x.text:
                obs = x.text
                obesitylist.append(float(obs.strip()))
    obesitylist=obesitylist[:191]           

    toopList = []
    for index in range(len(obesitylist)):
        toop = (realcountry[index], obesitylist[index])
        toopList.append(toop)
    return toopList


#Getting ID for Country
def GetCountryID():
    data = getObesityData()
    idDic = {}
    country_id = 0
    for country in data:
        country_id+= 1
        idDic[country[0]] = country_id
    return idDic

#Main DataBase
def createDB(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
        
    cur.execute('CREATE TABLE IF NOT EXISTS ObesityData (Country_ID INTEGER, ObesityRate FLOAT)')
    conn.commit()
    return cur, conn
#Country and ID Database
def addCountryTable(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS CountryID (Country_ID INTEGER PRIMARY KEY, Country TEXT)')
    conn.commit()
    return cur, conn

def addData(db_name):
    cur, conn = createDB(db_name)
    data = getObesityData()
    idDic = GetCountryID()

    for tup in data:
        try:
            country_id = idDic[tup[0]]
            obesityRate = tup[1]
        except:
            country_id = 0
            obesityRate = 0
        cur.execute('INSERT OR IGNORE INTO ObesityData (Country_ID, ObesityRate) VALUES (?, ?)', (country_id, obesityRate))
    conn.commit()

    cur, conn = addCountryTable(db_name)

    for country, id in idDic.items():
        cur.execute('INSERT OR IGNORE INTO CountryID (Country_ID, Country) VALUES (?, ?)', (id, country))
    conn.commit()

def main():
    db_name = "CovidObesityProject"
    getObesityData()
    GetCountryID()
    createDB(db_name)
    addCountryTable(db_name)
    addData(db_name)

main()




