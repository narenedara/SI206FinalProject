import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
def openDatabase(db_name = 'CovidObesityProject'):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
def getMainData(cur,con):
    

    avgData = []
    
    cur.execute(
            """
            SELECT CountryID.Country, PovertyRankData.PovertyRank,ObesityData.ObesityRate, CovidData.TotalCases,CovidData.TotalDeaths
            FROM CountryID
            JOIN CovidData ON CovidData.Country_ID = CountryID.Country_ID
            JOIN ObesityData on ObesityData.Country_ID=CovidData.Country_ID
            JOIN PovertyRankData on PovertyRankData.Country_ID=ObesityData.Country_ID           
            """)
    data = cur.fetchall()
    return data

def deathRates(data):
    newList =[]
    for toop in data:
        if toop[3] == 0:
            rate = 0
        else:
            rate = round((toop[4]/toop[3]) * 100, 2)
        newT = (toop[0], rate)
        newList.append(newT)
    return newList

def writefile(data):
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '/deathrates.txt', 'w') as f:
        f.write("Country, " + "Death Rates\n" )
        for toop in data:
            f.write(toop[0] + ", " + str(toop[1]) + '\n')
def ObesityDeathRateScatter(data):
    obesitylist=[]
    deathratelist=[]
    for country in data:
        if country[3] == 0:
            rate = 0
        else:
            rate = round((country[4]/country[3]) * 100, 2)
        obesitylist.append(country[2])
        deathratelist.append(rate)
    x = np.array(obesitylist)
    y = np.array(deathratelist)

    plt.scatter(x, y, color='red')
    plt.xlim([0, 40])
    plt.ylim([0,10])
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x))
    plt.title('Obesity Rate and Death Rate Scatterplot')
    plt.xlabel('Obesity Rate (%)')
    plt.ylabel('Death Rate (%)')

    plt.show()

def PovertyDeathRateScatter(data):
    povertylist=[]
    deathratelist=[]
    for country in data:
        if country[3] == 0:
            rate = 0
        else:
            rate = round((country[4]/country[3]) * 100, 2)
        povertylist.append(country[1])
        deathratelist.append(rate)
    x = np.array(povertylist)
    y = np.array(deathratelist)

    plt.scatter(x, y, color='green')
    # plt.xlim([0, 40])
    plt.ylim([0,8])
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x))
    plt.title('Poverty Rank and Death Rate Scatterplot')
    plt.xlabel('Poverty Rank')
    plt.ylabel('Death Rate (%)')

    plt.show()

def Top10DeathRate(data): 
    tuplist=[]
    for country in data:
        if country[3] == 0:
            rate = 0
        else:
            rate = round((country[4]/country[3]) * 100, 2)
        tup=(country[0],rate)
        tuplist.append(tup)
    tuplist.sort(key=lambda y: y[1], reverse=True)
    #print(tuplist)
    tuplist10=tuplist[:10]
    
    namelist=[]
    ratelist=[]
    for x in tuplist10:
        namelist.append(x[0])
        ratelist.append(x[1])
    x=np.array(namelist)
    y=np.array(ratelist)

    
    plt.barh(x, y)
    plt.title('Top 10 Death Rate')
    plt.xlabel('Death Rate')
    plt.ylabel('Countries')

    plt.show()




def bottom10DeathRate(data): 
    tuplist=[]
    for country in data:
        if country[3] == 0:
            rate = 0
        else:
            rate = round((country[4]/country[3]) * 100, 2)
        tup=(country[0],rate)
        tuplist.append(tup)
    tuplist.sort(key=lambda y: y[1])
    #print(tuplist)
    tuplist10=tuplist[:10]

    namelist=[]
    ratelist=[]
    for x in tuplist10:
        namelist.append(x[0])
        ratelist.append(x[1])
    x=np.array(namelist)
    y=np.array(ratelist)


    plt.barh(x, y, color='orange')
    plt.title('Bottom 10 Death Rate')
    plt.xlabel('Death Rate')
    plt.ylabel('Countries')

    plt.show()
def PovertyObesityScatter(data):
    povertylist=[]
    obesitylist=[]
    for country in data:
        povertylist.append(country[1])
        obesitylist.append(country[2])
    x = np.array(povertylist)
    y = np.array(obesitylist)

    plt.scatter(x, y, color='purple')
    # plt.xlim([0, 40])
    # plt.ylim([0,8])
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x))
    plt.title('Poverty Rank and Obesity Rate Scatterplot')
    plt.xlabel('Poverty Rank (lower is poorer')
    plt.ylabel('Obesity Rate (%)')

    plt.show()
def Top10PovertyRate(data): 
    tuplist=[]
    for country in data:
        tup=(country[0],country[1])
        tuplist.append(tup)
    tuplist.sort(key=lambda y: y[1])
    #print(tuplist)
    tuplist10=tuplist[:10]
    
    namelist=[]
    povertylist=[]
    for x in tuplist10:
        namelist.append(x[0])
        povertylist.append(x[1])
    x=np.array(namelist)
    y=np.array(povertylist)

    
    plt.barh(x, y, color="red")
    plt.title('Top 10 Poverty Rate')
    plt.xlabel('Poverty Rank(lower means poorer)')
    plt.ylabel('Countries')

    plt.show()
        


def main():
    c,d=openDatabase()
    da = getMainData(c,d)
    rat = deathRates(da)
    writefile(rat)
    ObesityDeathRateScatter(da)
    PovertyDeathRateScatter(da)
    Top10DeathRate(da)
    bottom10DeathRate(da)
    PovertyObesityScatter(da)
    Top10PovertyRate(da)
main()

