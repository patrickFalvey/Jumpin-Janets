import time
from time import strftime, gmtime, localtime, strptime, sleep
from datetime import *
from bs4 import BeautifulSoup
import requests
import dicttoxml
from xml.etree.ElementTree import *


gameList = []
gametime = []
awayTeams = []
homeTeams = []
teams=[]
scores=[]
clean={}


d = date.today() + timedelta(days=1)
tomDateFile = datetime.strftime(d,'%Y%m%d')
tomDateGame = datetime.strftime(d,'%m/%d/%y')
tomDateGame = tomDateGame[1:]
##url='http://scores.espn.go.com/ncb/scoreboard?date=' + tomDateFile
url='http://scores.espn.go.com/ncb/scoreboard?date=20150326'
currentTime=strftime('%H%M',localtime())
fileDate=strftime('%Y%m%d',localtime())
dayOfWeek=strftime('%A',localtime())

def scrape(website):
    r=requests.get(website)
    soup=BeautifulSoup(r.content)
    team=soup.select('p span a')
    score=soup.find_all('li',{'class':'final'})
    hometeam = soup.find_all('div', {'class':'team home'})
    gameStatus = soup.find_all('div',{'class':'game-status'})
    awayteam = soup.find_all('div', {'class':'team visitor'})
    gamedate = soup.find_all('h2')
    

    return team,score,gameStatus,awayteam,hometeam,gamedate


def dataScrub(team,score,gameStatus,awayteam,hometeam,gamedate):
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
            timeStamp = stat.contents[0].text
            timeStamp = timeStamp[:-3]
            
            gametime.append(timeStamp)
        
    for i in range(len(gameStatus)):
        num = 'game' + str(i + 1)
        gameList.append(num)
    for i in range(len(team)):
                clean[teams[i]]=scores[i]
    for i in gamedate:
        global gameday
        gameday = i.text[11:]
    
def makeSchedule(gameList,scores,homeTeams,awayTeams,teams,gametime,gameday):
    score = Element('schedule')
    week = SubElement(score,'week')
    week.attrib['weeknumber'] = 'week1'

    for i in range(len(gameList)):           
        game = Element('game')
        game.attrib['gameNumber']=gameList[i]
        hometeam = SubElement(game, 'hometeam')
        hometeam.text = homeTeams[i]
        awayteam = SubElement(game, 'awayteam')
        awayteam.text = awayTeams[i]
        gameTime = SubElement(game, 'gametime')
        gameTime.text = gametime[i]
        week.insert(i,game)
        startdate = SubElement(game, 'startdate')
        startdate.text = tomDateGame
        
##    bye = Element('bye')
##    none = SubElement(bye, 'none')
##    day.insert(len(gameList),bye)
    xmlFile = tostring(score)
    print xmlFile
    with open('scheduleFile'+fileDate+'.xml','w') as scoreData:
        scoreData.write(str(xmlFile))
        
        
team,score,gameStatus,awayteam,hometeam,gamedate = scrape(url)
dataScrub(team,score,gameStatus,awayteam,hometeam,gamedate)
def gamesCheck(gameList,scores,homeTeams,awayTeams,teams,gametime,gameday):
    if len(gameList) != 0:
        makeSchedule(gameList,scores,homeTeams,awayTeams,teams,gametime,gameday)       
    else:
        print 'No games tomorrow'
        sleep(18000)
        gamesCheck(gameList,scores,homeTeams,awayTeams,teams,gametime,gameday)
gamesCheck(gameList,scores,homeTeams,awayTeams,teams,gametime,gameday)

