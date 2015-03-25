import time
import datetime 
from bs4 import BeautifulSoup
import requests
import dicttoxml
from xml.etree.ElementTree import *
##import xml.etree.ElementTree as ET

gameList = []
gametime = []
awayTeams = []
homeTeams = []
teams=[]
scores=[]
clean={}
url="http://scores.espn.go.com/ncb/scoreboard?date=20150321"
def startScrape():
    while True:
        currentTime=time.strftime('%I:%M %p',time.localtime())
        currentDate=time.strftime('%m/%d/%Y',time.localtime())
        def scrape(website):
            r=requests.get(website)
            soup=BeautifulSoup(r.content)
            team=soup.select('p span a')
            score=soup.find_all('li',{'class':'final'})
            hometeam = soup.find_all('div', {'class':'team home'})
            gameStatus = soup.find_all('div',{'class':'game-status'})
            awayteam = soup.find_all('div', {'class':'team visitor'})    
            return team,score,gameStatus,awayteam,hometeam


        def dataScrub(team,score,gameStatus,awayteam,hometeam):
            for i in hometeam:
                links = i.find_all('a')
                for i in links:
                     teamName = i.get('title')
                     if teamName != None:
                         homeTeams.append(teamName)
            for i in awayteam:
                links = i.find_all('a')
                for i in links:
                     teamName = i.get('title')
                     if teamName != None:
                         awayTeams.append(teamName)
            for name in awayTeams:
                teams.append(name)
            for name in homeTeams:
                teams.append(name)
            for num in score:
                scores.append(num.text)    
            for i in scores:
                if i=='T':
                    scores.remove(i)
            for stat in gameStatus:
                if 'Final' in stat.contents[0].text:
                    over = 'Final'
                    gametime.append(over)
                else:
                    gametime.append(stat.contents[0].text)
                
            for i in range(len(gameStatus)):
                num = 'game' + str(i + 1)
                gameList.append(num)
            for i in range(len(team)):
                        clean[teams[i]]=scores[i]

            
        def makeSchedule(gameList,scores,homeTeams,awayTeams,teams,gametime):
            scheduleList = []
            score = Element('score')
            score.attrib['filedate'] = currentDate
            score.attrib['filetime'] = currentTime
            game = SubElement(score, 'game')
            game.attrib['hometeam']= homeTeams[0]
            game.attrib['awayteam']= awayTeams[0]
            awayscore = SubElement(game, 'awayscore')
            awayscore.text = clean[awayTeams[0]]
            homescore = SubElement(game, 'homescore')
            homescore.text = clean[homeTeams[0]]
            gameTime = SubElement(game, 'gametime')
            gameTime.text = gametime[0]
            
            for i in range(1,len(gameList)):           
                game = Element('game')
                game.attrib['hometeam']= homeTeams[i]
                game.attrib['awayteam']= awayTeams[i]
                awayscore = SubElement(game, 'awayscore')
                awayscore.text = clean[awayTeams[i]]
                homescore = SubElement(game, 'homescore')
                homescore.text = clean[homeTeams[i]]
                gameTime = SubElement(game, 'gametime')
                gameTime.text = gametime[i]
                score.append(game)
            xmlFile = tostring(score)
            print xmlFile
            fileTime=time.strftime('%H%M',time.localtime())
            with open('scoreFile'+fileTime+'.xml','w') as scoreData:
                scoreData.write(str(xmlFile))
            
               
        team,score,gameStatus,awayteam,hometeam = scrape(url)
        dataScrub(team,score,gameStatus,awayteam,hometeam)
        def gamesCheck(gameList,scores,homeTeams,awayTeams,teams,gametime):
            if len(gameList) != 0:
                makeSchedule(gameList,scores,homeTeams,awayTeams,teams,gametime)       
            else:
                return -1
        gamesCheck(gameList,scores,homeTeams,awayTeams,teams,gametime)
        time.sleep(65)





while True:
    d = datetime.date.today()
    currentDate = datetime.date.strftime(d,'%Y%m%d')
    currentTime=time.strftime('%H%M',time.localtime())
    print currentTime
    timeList = []
    tree=parse('scheduleFile'+currentDate+'.xml')
    root=tree.getroot()
    for gametime in root.iter('gametime'):
        roughTime = gametime.text
        timestring = time.strptime(roughTime, '%I:%M %p')
        gameTime=time.strftime('%H%M',timestring)
        print gameTime
        timeList.append(gameTime)
    for clock in timeList:
        if int(currentTime) > int(clock):
            print 'Scraping Web at ' + str(currentTime)
            startScrape()
            break
        else:
            print "Game hasn't started yet.  I'll wait another minute"
    time.sleep(60)
