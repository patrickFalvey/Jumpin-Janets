import time
import xml.etree.ElementTree as ET
from time import strftime, gmtime, localtime
from bs4 import BeautifulSoup
import dicttoxml
import requests
import sys


scores=[]
newScores=[]
teams=[]
clean={}
url="http://scores.espn.go.com/ncb/scoreboard"

def startScrape():
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
        time.sleep(60)


while True:   
    currentTime=int(strftime('%H%M',localtime()))
##    currentTime=int(currentTime)
    tree=ET.parse('scheduleData.xml')
    root=tree.getroot()

    gameTime=int(root[0][0].text)
##    gameTime=int(gameTime)

    if currentTime >= gameTime:
        print 'Scraping Web at ' + str(currentTime)
        startScrape()
        break
    else:
        print "Game hasn't started yet.  I'll wait another minute"
        time.sleep(60)
