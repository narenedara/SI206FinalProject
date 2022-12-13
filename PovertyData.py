import requests
import json
from bs4 import BeautifulSoup
import os
import sqlite3

def getPovertyData():
    url="https://www.indexmundi.com/g/r.aspx?v=69"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    country = []


    table2= soup.find_all('a')
    for x in table2:
        country.append(x.text)
    country=country[3:175]
    country[10] = "Democratic Republic of the Congo"
    country[23] = "Gambia"
    country[28] = "Republic of the Congo"
    country[71] = "Federated States of Micronesia"
    country[134] = "South Korea"
    country[151] = "Bahamas"



    toopList = []
    rank = 1
    for count in country:
        toop = (count, rank)
        toopList.append(toop)
        rank += 1
    return toopList
    print(toopList)
def AssignID(toopList,db_name):
    lis = {}
    conn = sqlite3.connect('/Users/narenedara/Desktop/si206/FinalProject206/CovidObesityProject')
    cur=conn.cursor()
    dicti = cur.execute('SELECT * FROM CountryID')
    finallist=[]

    for item in dicti:
        lis[item[1]] = item[0]
    for toop in toopList:
        if toop[0] in lis.keys():
            deez=(lis[toop[0]],toop[1])
            finallist.append(deez)
    return finallist


    


def createDB(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
        
    cur.execute('CREATE TABLE IF NOT EXISTS PovertyRankData (Country_ID INTEGER, PovertyRank INTEGER)')
    conn.commit()
    return cur, conn


def addData(db_name, data, cur, conn):
    
    
    

    for tup in data:
        try:
            country_id = tup[0]
            PovertyRank = tup[1]
        except:
            country_id = 0
            PovertyRank= 0
        cur.execute('INSERT OR IGNORE INTO PovertyRankData (Country_ID, PovertyRank) VALUES (?, ?)', (country_id, PovertyRank))
    conn.commit()

def main():
    db_name = "CovidObesityProject"
    toop=getPovertyData()
    c, d = createDB(db_name)
    data = AssignID(toop, db_name)
    addData(db_name, data, c, d)

main()

