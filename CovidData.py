import requests
import json
import os
import sqlite3



def getAPISQL():
    lis = []
    conn = sqlite3.connect('/Users/narenedara/Desktop/si206/FinalProject206/APIDataStored')
    cur=conn.cursor()
    dicti = cur.execute('SELECT * FROM APIdata')
    for item in dicti:
        lis.append(item)

    return lis


def AssignID(toopList):
    lis = {}
    conn = sqlite3.connect('/Users/narenedara/Desktop/si206/FinalProject206/CovidObesityProject')
    cur=conn.cursor()
    dicti = cur.execute('SELECT * FROM CountryID')
    finallist=[]

    for item in dicti:
        lis[item[1]] = item[0]
    for toop in toopList:
        if toop[0] in lis.keys():
            deez=(lis[toop[0]],toop[1],toop[2])
            finallist.append(deez)
    return finallist

def createDB(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
        
    cur.execute('CREATE TABLE IF NOT EXISTS CovidData (Country_ID INTEGER, TotalCases INTEGER, TotalDeaths INTEGER)')
    conn.commit()
    return cur, conn



def addData(db_name, data, cur, conn):
    cur.execute("SELECT COUNT(*) as Counter FROM CovidData")
    result = cur.fetchall()

    rowCount = result[0][0]
    maxRows = rowCount + 25
    idx = rowCount - 1
    while rowCount < maxRows and rowCount < 169:
        tooply = data[idx]
        try:
            country_id = tooply[0]
            TotalCases = tooply[1]
            TotalDeaths=tooply[2]
        except:
            country_id = 0
            TotalCases = 0
            TotalDeaths=0
        cur.execute('INSERT OR IGNORE INTO  CovidData (Country_ID, TotalCases, TotalDeaths) VALUES (?, ?, ?)', (country_id, TotalCases,TotalDeaths))
        cur.execute("SELECT COUNT(*) as Counter FROM CovidData")
        idx += 1
        result = cur.fetchall()
        rowCount = result[0][0]
    conn.commit()

def main():
    db_name = "CovidObesityProject"
    api_name = "APIDataStored"
    api = getAPISQL()
    c, d = createDB(db_name)
    data = AssignID(api)
    addData(db_name, data, c, d)

main()

