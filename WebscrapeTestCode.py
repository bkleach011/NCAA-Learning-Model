import os
import random as rand
import requests
import string
import time
import traceback
from bs4 import BeautifulSoup
from datetime import timedelta, date

def ConvertTeamNames(list): #Convert NCAA bracket names to Sports Reference Names
    for teami in range(0,len(list)):
        if list[teami][-3:] == 'St.':
            list[teami] = list[teami][:-3] + 'State'
        if list[teami][-2:] == 'CC':
            list[teami] = list[teami][:-2] + 'Corpus Christi'
        if list[teami] == 'Charleston':
            list[teami] = 'College of Charleston'
        if list[teami] == 'Western Ky.':
            list[teami] = 'Western Kentucky'
        if list[teami] == 'Grambling State':
            list[teami] = 'Grambling'
        if list[teami] == "St. John's":
            list[teami] = "St. John's (NY)"
        if list[teami] == 'UCSB':
            list[teami] = 'UC Santa Barbara'
        if list[teami] == 'F. Dickinson':
            list[teami] = 'FDU'
        if list[teami] == 'FAU':
            list[teami] = 'Florida Atlantic'
        if list[teami] == 'USC':
            list[teami] = 'Southern California'
        if list[teami] == 'N Kentucky':
            list[teami] = 'Northern Kentucky'
        if list[teami] == 'Pitt':
            list[teami] = 'Pittsburgh'
        if list[teami] == 'VCU':
            list[teami] = 'Virginia Commonwealth'
        if list[teami] == 'UConn':
            list[teami] = 'Connecticut'
        if list[teami] == 'Loyola Chicago':
            list[teami] = 'Loyola (IL)'
        if list[teami] == 'LSU':
            list[teami] = 'Louisiana State'
        if list[teami] == 'Eastern Wash.':
            list[teami] = 'Eastern Washington'
        if list[teami] == 'MSM/TXSO':
            list[teami] = 'Texas Southern'
        if list[teami] == 'BYU':
            list[teami] = 'Brigham Young'
        if list[teami] == 'MSU/UCLA':
            list[teami] = 'UCLA'
        if list[teami] == 'Ole Miss':
            list[teami] = 'Mississippi'
        if list[teami] == 'UMBC':
            list[teami] = 'Maryland-Baltimore County'
        if list[teami] == 'Cal St. Fullerton':
            list[teami] = 'Cal State Fullerton'
        if list[teami] == 'Penn':
            list[teami] = 'Pennsylvania'
        if list[teami] == 'East Tenn. State':
            list[teami] = 'East Tennessee State'
        if list[teami] == 'Penn':
            list[teami] = 'Pennsylvania'
        if list[teami] == 'SMU':
            list[teami] = 'Southern Methodist'
        if list[teami] == 'Penn':
            list[teami] = 'Pennsylvania'
        if list[teami] == 'Fla. Gulf Coast':
            list[teami] = 'Florida Gulf Coast'
        if list[teami] == 'Middle Tenn.':
            list[teami] = 'Middle Tennessee'
        if list[teami] == 'CSU Bakersfield':
            list[teami] = 'Cal State Bakersfield'
        if list[teami] == 'TCU':
            list[teami] = 'Texas Christian'
        if list[teami] == 'Cal Baptist':
            list[teami] = 'California Baptist'
        if list[teami] == 'Long Island':
            list[teami] = 'Long Island University'
        if list[teami] == 'Queens (N.C.)':
            list[teami] = 'Queens (NC)'
        if list[teami] == 'Miami (Ohio)':
            list[teami] = 'Miami (OH)'
            
    return list

delay = 5
time.sleep(delay) #So the websites don't get ddosed lol
r = requests.get('https://www.ncaa.com/march-madness-live/bracket')
soup = BeautifulSoup(r.content, 'html.parser')

topregions = soup.find('div', class_ = "regions top")
bottomregions = soup.find('div', class_ = "regions bottom")
tlreg = topregions.find('div', class_ = "region region-left")
trreg = topregions.find('div', class_ = "region region-right")
blreg = bottomregions.find('div', class_ = "region region-left")
brreg = bottomregions.find('div', class_ = "region region-right")

teams = []
for team in tlreg.find('div', class_ = "region-round round-1").find_all('p', class_ = 'body body_2 color_lvl_-5'):
    teams.append(team.text)
for team in trreg.find('div', class_ = "region-round round-1").find_all('p', class_ = 'body body_2 color_lvl_-5'):
    teams.append(team.text)
for team in blreg.find('div', class_ = "region-round round-1").find_all('p', class_ = 'body body_2 color_lvl_-5'):
    teams.append(team.text)
for team in brreg.find('div', class_ = "region-round round-1").find_all('p', class_ = 'body body_2 color_lvl_-5'):
    teams.append(team.text)

del teams[1::2]
print(teams)

time.sleep(delay) #So the websites don't get ddosed lol
link = requests.get(f'https://www.sports-reference.com/cbb/seasons/men/{date.today().year}-school-stats.html')
soup = BeautifulSoup(link.content, 'html.parser')
schools = soup.find_all('td', attrs={"data-stat": "school_name"})
srrows = [] #sports reference rows
notfoundteams = []
for team in teams:
    found = False
    for school in schools:
        if school.find('a').text == team:
            srrows.append(school.find_parent('tr'))
            found = True
    if not found:
        notfoundteams.append(team)

print(srrows[0].find('td', attrs={"data-stat": "fg_pct"}).text)