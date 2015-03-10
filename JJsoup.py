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


    # Save data to disk
    def saveData(cleanxml):
        scoreData=open('scoreData.xml','w')
        scoreData=scoreData.write(str(cleanxml))
        
        
    team,score=scrape(url)    
    saveData(dataScrub(team,score))
    time.sleep(300)



    




