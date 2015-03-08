import requests
from bs4 import BeautifulSoup
import sys

url = "http://scores.espn.go.com/ncb/scoreboard"

r = requests.get(url)
soup = BeautifulSoup(r.content)
team = soup.find_all('p',{'class':'team-name'})
score = soup.find_all('li',{'class':'final'})
scores = []
newScores = []
teams = []
for name in team:
    teams.append(name.text)
for num in score:
    scores.append(num.text)
print(scores)
for i in scores:
    if i == 'T':
        scores.remove(i)
clean = {}
for i in range(len(team)):
    clean[teams[i]] = scores[i]
print(clean)
file = open('scoreData.txt','w')
file = file.write(str(clean))
    



