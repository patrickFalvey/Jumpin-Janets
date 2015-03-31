import time
import datetime 
from bs4 import BeautifulSoup
import requests
import dicttoxml
from xml.etree.ElementTree import *
import sys
import pytz

d = datetime.date.today()
fileDate = datetime.date.strftime(d,'%Y%m%d')

def startScrape():
    while True:
        awayPlayingScheduled = []
        homePlayingScheduled = []
        awayNotPlayingScheduled = []
        homeNotPlayingScheduled = []
        finalList = []
        gameList = []
        gametime = []
        awayTeams = []
        homeTeams = []
        teams=[]
        scores=[]
        clean={}
        currentTime=time.strftime('%I:%M %p',time.localtime())
        currentDate=time.strftime('%m/%d/%Y',time.localtime())
##        url="http://scores.espn.go.com/ncb/scoreboard?date=" + fileDate
        url="http://scores.espn.go.com/ncb/scoreboard?date=20150320"
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
            for i in homeTeams:
                print 'hometeam = ' + i
                if i in teamsScheduledHome:
                    homePlayingScheduled.append(i)
                else:
                    pass
            for i in teamsScheduledHome:
                if i not in homeTeams:
                    homeNotPlayingScheduled.append(i)
                else:
                    pass               
            for i in awayTeams:
                if i in teamsScheduledAway:
                    print "I'm in!"
                    awayPlayingScheduled.append(i)
                else:
                    pass
            for i in teamsScheduledAway:
                if i not in awayTeams:
                    awayNotPlayingScheduled.append(i)
                else:
                    pass 
            
            for num in score:
                scores.append(num.text)    
            for i in scores:
                if i=='T':
                    scores.remove(i)
            for i in range(len(awayTeams)):
                teams.append(awayTeams[i])
                teams.append(homeTeams[i])
                
            for stat in gameStatus:
                if 'Final' in stat.contents[0].text:
                    over = 'Final'
                    gametime.append(over)
                else:
                    gametime.append(stat.contents[0].text)
            for stat in gametime:
                if stat == 'Final':
                    finalList.append(stat)
                else:
                    pass    
            for i in range(len(gametime)):
                num = 'game' + str(i + 1)
                gameList.append(num)
            for i in range(len(team)):
                        clean[teams[i]]=scores[i]
##            print clean
            
        def makeSchedule(gameList,scores,homeTeams,awayTeams,teams,gametime,awayPlayingScheduled,homePlayingScheduled,awayNotPlayingScheduled,homeNotPlayingScheduled):
            scheduleList = []
            score = Element('score')
            score.attrib['filedate'] = currentDate
            score.attrib['filetime'] = currentTime
            game = SubElement(score, 'game')
            game.attrib['hometeam']= homePlayingScheduled[0]
            game.attrib['awayteam']= awayPlayingScheduled[0]
            awayscore = SubElement(game, 'awayscore')
            awayscore.text = clean[awayPlayingScheduled[0]]
            homescore = SubElement(game, 'homescore')
            homescore.text = clean[homePlayingScheduled[0]]
            gameTime = SubElement(game, 'starttime')
            gameTime.text = gametime[0]
            
            for i in range(1,len(homePlayingScheduled)):           
                game = Element('game')
                game.attrib['hometeam']= homePlayingScheduled[i]
                game.attrib['awayteam']= awayPlayingScheduled[i]
                awayscore = SubElement(game, 'awayscore')
                awayscore.text = clean[awayPlayingScheduled[i]]
                homescore = SubElement(game, 'homescore')
                homescore.text = clean[homePlayingScheduled[i]]
                gameTime = SubElement(game, 'starttime')
                gameTime.text = gametime[i]
                score.append(game)
                
            for i in range(len(awayNotPlayingScheduled)):           
                game = Element('game')
                game.attrib['hometeam']= homeNotPlayingScheduled[i]
                game.attrib['awayteam']= awayNotPlayingScheduled[i]
                awayscore = SubElement(game, 'awayscore')
                awayscore.text = '0'
                homescore = SubElement(game, 'homescore')
                homescore.text = '0'
                gameTime = SubElement(game, 'starttime')
                gameTime.text = 'Not Yet'
                score.append(game)
            xmlFile = tostring(score)
            print xmlFile
            fileTime=time.strftime('%H%M',time.localtime())
            with open('scoreFile'+fileTime+'.xml','w') as scoreData:
                scoreData.write(str(xmlFile))
            with open('scoreFile.xml','w') as scoreData:
                scoreData.write(str(xmlFile))
            
               
        team,score,gameStatus,awayteam,hometeam = scrape(url)
        dataScrub(team,score,gameStatus,awayteam,hometeam)
        def gamesCheck(gameList,scores,homeTeams,awayTeams,teams,gametime,awayPlayingScheduled,homePlayingScheduled,awayNotPlayingScheduled,homeNotPlayingScheduled):
            if len(gameList) != 0:
                makeSchedule(gameList,scores,homeTeams,awayTeams,teams,gametime,awayPlayingScheduled,homePlayingScheduled,awayNotPlayingScheduled,homeNotPlayingScheduled)       
            else:
                print 'No games playing today'
                time.sleep(3600)
        gamesCheck(gameList,scores,homeTeams,awayTeams,teams,gametime,awayPlayingScheduled,homePlayingScheduled,awayNotPlayingScheduled,homeNotPlayingScheduled)
        time.sleep(65)


while True:     
    currentTime=time.strftime('%H%M',time.localtime())
    print currentTime
    count = 0
    timeList = []
    gamesOver = []
    teamsScheduledHome = []
    teamsScheduledAway = []
    tree=parse('scheduleFile'+fileDate+'.xml')
    root=tree.getroot()
    for team in root.iter('awayTeam'):
        teamsScheduledAway.append(team.text)
        print team.text
    for team in root.iter('homeTeam'):
        teamsScheduledHome.append(team.text)
        print team.text
    for gametime in root.iter('startTime'):
        count+=1
        roughTime = gametime.text
        if roughTime == 'Final':
            gamesOver.append(roughTime)
        else:           
            timestring = time.strptime(roughTime, '%I:%M %p')
            gameTime=time.strftime('%H%M',timestring)
            timeList.append(gameTime)
    for clock in timeList:
        if int(currentTime) > int(clock):
            print 'Scraping Web at ' + str(currentTime)
            startScrape()
            break
        else:
            print "Game hasn't started yet.  I'll wait another minute"
        time.sleep(3600)

