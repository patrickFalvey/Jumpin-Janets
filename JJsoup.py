import requests
from bs4 import BeautifulSoup
import dicttoxml
import sys
import re


scores=[]
newScores=[]
teams=[]
clean={}
url="http://scores.espn.go.com/ncb/scoreboard"
r=requests.get(url)
soup=BeautifulSoup(r.content)
team=soup.select('p span a')
score=soup.find_all('li',{'class':'final'})


for name in team:
    teams.append(name.text)
    
for num in score:
    scores.append(num.text)
    
for i in scores:
    if i=='T':
        scores.remove(i)
        
for i in range(len(team)):
    clean[teams[i]]=scores[i]
    
sweetness=dicttoxml.dicttoxml(clean)

file=open('scoreData.txt','w')
file=file.write(str(sweetness))
    




