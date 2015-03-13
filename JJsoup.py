from bs4 import BeautifulSoup
import dicttoxml
import requests
import time
import sys


scores=[]
newScores=[]
teams=[]
clean={}
url="http://scores.espn.go.com/ncb/scoreboard"


while True:
    # Scrape website with Beautiful Soup
    def scrape(website):
        r=requests.get(website)
        soup=BeautifulSoup(r.content)
        team=soup.select('p span a')
        score=soup.find_all('li',{'class':'final'})
        return team,score


    # Refine data and return it in XML format
    def dataScrub(x,y):
        dopexml = ''
        for name in x:
            teams.append(name.text)    
        for num in y:
            scores.append(num.text)    
        for i in scores:
            if i=='T':
                scores.remove(i)
        for i in range(len(team)):
            clean[teams[i]]=scores[i]
        cleanxml=dicttoxml.dicttoxml(clean)
        return cleanxml

    def filterxml(cleanxml):
        dopexml = ''
        for i in cleanxml:
            if i == '&':
                i = '&amp;'
                v = i
                dopexml = dopexml + v
            else:
                dopexml = dopexml + i
        print dopexml
        return dopexml


    # Save data to disk
    def saveData(dopexml):
        scoreData=open('scoreData.xml','w')
        scoreData=scoreData.write(dopexml)
        
        
    team,score=scrape(url)
    saveData(filterxml(dataScrub(team,score)))
    time.sleep(300)



    




