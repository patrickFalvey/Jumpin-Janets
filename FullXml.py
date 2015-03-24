import time
from time import strftime, gmtime, localtime
from bs4 import BeautifulSoup
import requests
import dicttoxml
from lxml import etree


gameList = []
gametime = []
awayTeams = []
homeTeams = []
teams=[]
scores=[]
clean={}
url="http://scores.espn.go.com/ncb/scoreboard?date=20150321"


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
        gametime.append(stat.contents[0].text)
    for i in range(len(gameStatus)):
        num = 'game' + str(i + 1)
        gameList.append(num)
    for i in range(len(team)):
                clean[teams[i]]=scores[i]
        
    print '\n\ngameList = \n\n' + str(gameList)
    print '\n\nscores = \n\n' + str(scores)
    print '\n\nhomeTeams = \n\n' + str(homeTeams)
    print '\n\nawayTeams = \n\n' + str(awayTeams)
    print '\n\nteams = \n\n' + str(teams)
    print '\n\ngametime = \n\n' + str(gametime)
    print '\n\nteam scores = \n\n' + str(clean)
    
    def makeSchedule(gameList,scores,homeTeams,awayTeams,teams,gametime):
        scheduleList = []
        for i in range(len(gameList)):
            schedule = {}
            schedule['hometeam'] = homeTeams[i]
            schedule['awayteam'] = awayTeams[i]
            schedule['homescore'] = clean[homeTeams[i]]
            schedule['awayscore'] = clean[awayTeams[i]]
            schedule['gametime'] = gametime[i]
            scheduleList.append(schedule)
        return scheduleList
        
        
    scheduleList = makeSchedule(gameList,scores,homeTeams,awayTeams,teams,gametime)       
    def makeXml(stats):
        xmlList = []
        root = dicttoxml.dicttoxml(scheduleList[0],custom_root='score',attr_type=False)
        base = etree.fromstring(root)
        for i in range(1,len(scheduleList)):
            xml = dicttoxml.dicttoxml(scheduleList[i],custom_root='game',attr_type=False)
            xml = etree.fromstring(xml)
            base.append(xml)
        print etree.tostring(base)
        xmlFile = etree.tostring(base)
        
        with open('scoreFile.xml','w') as scoreData:
            scoreData.write(str(xmlFile))
            
            
    makeXml(scheduleList)
            
        
        
team,score,gameStatus,awayteam,hometeam = scrape(url)
dataScrub(team,score,gameStatus,awayteam,hometeam)
