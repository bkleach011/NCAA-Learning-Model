#---------- Imports ----------#

import os
import random as rand
import requests
import string
import time
import traceback
from bs4 import BeautifulSoup
from datetime import timedelta, date

from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

#---------- Model Initializer ----------#

# Data Learning #
dataset = []
model = None
scaler = None

#---------- Initalized Lists and Variables ----------#

year = 2016 #NO LOWER THAN 2016
startyear = year
delay = 5

# Basic Stats #

# Advanced Stats #
srs = 0
sos = 0
fgpct = 0
fg3pct = 0
ftpct = 0
trb = 0
ast = 0
stl = 0

# Total Counts #
tsrs = 0
tsos = 0
tfgpct = 0
tfg3pct = 0
tftpct = 0
ttrb = 0
tast = 0
tstl = 0

#---------- Pathing Fix ----------#

dir_path = os.path.dirname(os.path.realpath(__file__))
pathlist = [*dir_path]
path = ""
for i in range(len(pathlist)):
    if pathlist[i] == '\\':
        pathlist[i] = "/"
    path += pathlist[i]

#---------- Functions ----------#

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

def UpdateCommons(stats):
    global srs
    global sos
    global fgpct
    global fg3pct
    global ftpct
    global trb
    global ast
    global stl
    global tsrs
    global tsos
    global tfgpct
    global tfg3pct
    global tftpct
    global ttrb
    global tast
    global tstl
    for stat in stats:
        match stat:
            case 'srs':
                srs += 1
                tsrs += 1
            case 'sos':
                sos += 1
                tsos += 1
            case 'fg_pct':
                fgpct += 1
                tfgpct += 1
            case 'fg3_pct':
                fg3pct += 1
                tfg3pct += 1
            case 'ft_pct':
                ftpct += 1
                tftpct += 1
            case 'trb': #get avg
                trb += 1
                ttrb += 1
            case 'ast': #get avg
                ast += 1
                tast += 1
            case 'stl': #get avg
                stl += 1
                tstl += 1
            case _:
                pass

def ExtractStats(row, orow, seed):
    stats = {
        "seed": seed,
        "srs": float(row.find('td', attrs={"data-stat": "srs"}).text),
        "sos": float(row.find('td', attrs={"data-stat": "sos"}).text),
        "fg_pct": float(row.find('td', attrs={"data-stat": "fg_pct"}).text),
        # "fg3_pct": float(row.find('td', attrs={"data-stat": "fg3_pct"}).text),
        "ft_pct": float(row.find('td', attrs={"data-stat": "ft_pct"}).text),
        "trb_pg": float(row.find('td', attrs={"data-stat": "trb"}).text) / float(row.find('td', attrs={"data-stat": "g"}).text),
        # "ast_pg": float(row.find('td', attrs={"data-stat": "ast"}).text) / float(row.find('td', attrs={"data-stat": "g"}).text),
        "tov_pg": float(row.find('td', attrs={"data-stat": "tov"}).text) / float(row.find('td', attrs={"data-stat": "g"}).text),
        "pts_allowed_pg": float(orow.find('td', attrs={"data-stat": "opp_pts"}).text) / float(row.find('td', attrs={"data-stat": "g"}).text),  # Opp PTS / games
        "opp_fg_pct": float(orow.find('td', attrs={"data-stat": "opp_fg_pct"}).text),
        "opp_tov_pg": float(orow.find('td', attrs={"data-stat": "opp_tov"}).text) / float(row.find('td', attrs={"data-stat": "g"}).text),
        "point_diff": (float(row.find('td', attrs={"data-stat": "pts"}).text) / float(row.find('td', attrs={"data-stat": "g"}).text)) 
        - (float(orow.find('td', attrs={"data-stat": "opp_pts"}).text) / float(row.find('td', attrs={"data-stat": "g"}).text)),
        "tov_margin": (float(row.find('td', attrs={"data-stat": "tov"}).text) / float(row.find('td', attrs={"data-stat": "g"}).text)) 
        - (float(orow.find('td', attrs={"data-stat": "opp_tov"}).text) / float(row.find('td', attrs={"data-stat": "g"}).text)),
    }
    return stats

def CompareStats(roundteams, winners):
    global osrrows
    global srrows
    global seeds
    global dataset

    index = 0
    newsrrows = []
    newosrrows = []
    newseeds = []
    # print(len(seeds))
    if (len(roundteams) == 4):
        tempteams = []
        tempteams.append(roundteams[0])
        tempteams.append(roundteams[2])
        tempteams.append(roundteams[1])
        tempteams.append(roundteams[3])
        tempseeds = []
        tempseeds.append(seeds[0])
        tempseeds.append(seeds[2])
        tempseeds.append(seeds[1])
        tempseeds.append(seeds[3])
        tempsrrows = []
        tempsrrows.append(srrows[0])
        tempsrrows.append(srrows[2])
        tempsrrows.append(srrows[1])
        tempsrrows.append(srrows[3])
        temposrrows = []
        temposrrows.append(osrrows[0])
        temposrrows.append(osrrows[2])
        temposrrows.append(osrrows[1])
        temposrrows.append(osrrows[3])
        roundteams = tempteams
        seeds = tempseeds
        srrows = tempsrrows
        osrrows = temposrrows
        # print(roundteams)
        # print(seeds)
        # for row in srrows:
        #     print(row.find('a').text)
        # for orow in osrrows:
        #     print(orow.find('a').text)

    while index < len(roundteams)-1:
        if winners.count(roundteams[index]) == 1:
            winnerind = index
            loserind = index + 1
        else:
            winnerind = index + 1
            loserind = index

        newsrrows.append(srrows[winnerind])
        newosrrows.append(osrrows[winnerind])

        w_stats = ExtractStats(srrows[winnerind], osrrows[winnerind], seeds[winnerind])
        l_stats = ExtractStats(srrows[loserind], osrrows[loserind], seeds[loserind])
        newseeds.append(seeds[winnerind])

        # Build feature differences
        features = [
            l_stats["seed"] - w_stats["seed"],
            w_stats["srs"] - l_stats["srs"],
            w_stats["sos"] - l_stats["sos"],
            w_stats["fg_pct"] - l_stats["fg_pct"],
            # w_stats["fg3_pct"] - l_stats["fg3_pct"],
            w_stats["ft_pct"] - l_stats["ft_pct"],
            w_stats["trb_pg"] - l_stats["trb_pg"],
            # w_stats["ast_pg"] - l_stats["ast_pg"],
            l_stats["tov_pg"] - w_stats["tov_pg"],
            l_stats["pts_allowed_pg"] - w_stats["pts_allowed_pg"],
            l_stats["opp_fg_pct"] - w_stats["opp_fg_pct"],
            w_stats["opp_tov_pg"] - l_stats["opp_tov_pg"],
            w_stats["point_diff"] - l_stats["point_diff"],
            w_stats["tov_margin"] - l_stats["tov_margin"],
        ]

        # Winner = 1
        dataset.append((features, 1))

        # FLIP (VERY IMPORTANT)
        flipped = [-x for x in features]
        dataset.append((flipped, 0))

        index += 2
    osrrows = newosrrows
    srrows = newsrrows
    seeds = newseeds

def PredictGame(teamA, teamB):
    features = [
        teamB["seed"] - teamA["seed"],
        teamA["srs"] - teamB["srs"],
        teamA["sos"] - teamB["sos"],
        teamA["fg_pct"] - teamB["fg_pct"],
        # teamA["fg3_pct"] - teamB["fg3_pct"],
        teamA["ft_pct"] - teamB["ft_pct"],
        teamA["trb_pg"] - teamB["trb_pg"],
        # teamA["ast_pg"] - teamB["ast_pg"],
        teamB["tov_pg"] - teamA["tov_pg"],
        teamB["pts_allowed_pg"] - teamA["pts_allowed_pg"],
        teamB["opp_fg_pct"] - teamA["opp_fg_pct"],
        teamA["opp_tov_pg"] - teamB["opp_tov_pg"],
        teamA["point_diff"] - teamB["point_diff"],
        teamA["tov_margin"] - teamB["tov_margin"],
    ]

    features = scaler.transform([features])

    prob = model.predict_proba(features)[0][1] #Probability that teamA beats teamB
    return prob

def Pick_winner(teamA_name, teamA_stats, teamB_name, teamB_stats):
    probA = PredictGame(teamA_stats, teamB_stats)
    probB = PredictGame(teamB_stats, teamA_stats)

    if probA > probB:
        return teamA_name, teamB_name, probA
    else:
        return teamB_name, teamA_name, probB

def PredictRound(teamsremaining, statrows, ostatrows, seedsremaining):
    currentround = ""
    match len(teamsremaining):
        case 64:
            currentround = "Round 1"
        case 32:
            currentround = "Round 2"
        case 16:
            currentround = "the Sweet Sixteen"
        case 8:
            currentround = "the Elite Eight"
        case 4:
            currentround = "the Final Four"
        case 2:
            currentround = "the Championship"
        case _:
            raise ValueError("Impossible Round!")
        
    winners = []
    winnerrows = []
    winnerorows = []
    winnerseeds = []
    file.write(f"---------- {currentround} ----------\n\n")

    ind = 0
    while ind < len(teamsremaining)-1:
        winner, loser, confidence = Pick_winner(teamsremaining[ind], ExtractStats(statrows[ind], ostatrows[ind], seedsremaining[ind]), 
                                                teamsremaining[ind+1], ExtractStats(statrows[ind+1], ostatrows[ind+1], seedsremaining[ind+1]))
        if winner == teamsremaining[ind]:
            wseed = seedsremaining[ind]
            lseed = seedsremaining[ind+1]
        else:
            wseed = seedsremaining[ind+1]
            lseed = seedsremaining[ind]

        file.write(f"{winner} (No. {wseed}) should beat {loser} (No. {lseed}) ({100*confidence:.2f}% Chance) in {currentround}\n")
        if winner == teamsremaining[ind]:
            winners.append(teamsremaining[ind])
            winnerrows.append(statrows[ind])
            winnerorows.append(ostatrows[ind])
            winnerseeds.append(seedsremaining[ind])
        else:
            winners.append(teamsremaining[ind+1])
            winnerrows.append(statrows[ind+1])
            winnerorows.append(ostatrows[ind+1])
            winnerseeds.append(seedsremaining[ind+1])
        ind += 2
    if len(winners) == 4: #Matchups are incorrect going into final 4
        tempwinners = []
        tempwinners.append(winners[0])
        tempwinners.append(winners[2])
        tempwinners.append(winners[1])
        tempwinners.append(winners[3])
        temprows = []
        temprows.append(winnerrows[0])
        temprows.append(winnerrows[2])
        temprows.append(winnerrows[1])
        temprows.append(winnerrows[3])
        tempseeds = []
        tempseeds.append(winnerseeds[0])
        tempseeds.append(winnerseeds[2])
        tempseeds.append(winnerseeds[1])
        tempseeds.append(winnerseeds[3])
        temporows = []
        temporows.append(winnerorows[0])
        temporows.append(winnerorows[2])
        temporows.append(winnerorows[1])
        temporows.append(winnerorows[3])
        winners = tempwinners
        winnerrows = temprows
        winnerorows = temporows
        winnerseeds = tempseeds
        file.write("\n")
    elif len(winners) == 1: #added for readability
        pass
    else:
        file.write("\n")
    return winners, winnerrows, winnerorows, winnerseeds
        
#---------- Main Code ----------#

while year < date.today().year-1:
    srs = 0
    sos = 0
    fgpct = 0
    fg3pct = 0
    ftpct = 0
    trb = 0
    ast = 0
    stl = 0
    seeds = [1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,
             1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,
             1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,
             1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15
    ]
    if year != 2020:
        time.sleep(delay) #So the websites don't get ddosed lol
        r = requests.get(f'https://www.ncaa.com/brackets/basketball-men/d1/{year}#main-content')
        soup = BeautifulSoup(r.content, 'html.parser')
        regions = soup.find_all('div', class_ = "regions")
        topregions = regions[0]
        bottomregions = regions[1]
        tlreg = topregions.find('div', class_ = "region region-left")
        trreg = topregions.find('div', class_ = "region region-right")
        blreg = bottomregions.find('div', class_ = "region region-left")
        brreg = bottomregions.find('div', class_ = "region region-right")

        teams = []
        for team in tlreg.find('div', class_ = "round-1 region-round").find_all('span', class_ = 'name'):
            teams.append(team.text)
        for team in trreg.find('div', class_ = "round-1 region-round").find_all('span', class_ = 'name'):
            teams.append(team.text)
        for team in blreg.find('div', class_ = "round-1 region-round").find_all('span', class_ = 'name'):
            teams.append(team.text)
        for team in brreg.find('div', class_ = "round-1 region-round").find_all('span', class_ = 'name'):
            teams.append(team.text)
        ConvertTeamNames(teams)

        round1winners = [] #doubles as teams for round 2
        for winner in tlreg.find('div', class_ = "round-1 region-round").find_all('div', class_ = "team winner"):
            round1winners.append(winner.find('span', class_ = 'name').text)
        for winner in trreg.find('div', class_ = "round-1 region-round").find_all('div', class_ = "team winner"):
            round1winners.append(winner.find('span', class_ = 'name').text)
        for winner in blreg.find('div', class_ = "round-1 region-round").find_all('div', class_ = "team winner"):
            round1winners.append(winner.find('span', class_ = 'name').text)
        for winner in brreg.find('div', class_ = "round-1 region-round").find_all('div', class_ = "team winner"):
            round1winners.append(winner.find('span', class_ = 'name').text)
        ConvertTeamNames(round1winners)

        round2winners = [] #doubles as teams for round 3
        for winner in tlreg.find('div', class_ = "round-2 region-round").find_all('div', class_ = "team winner"):
            round2winners.append(winner.find('span', class_ = 'name').text)
        for winner in trreg.find('div', class_ = "round-2 region-round").find_all('div', class_ = "team winner"):
            round2winners.append(winner.find('span', class_ = 'name').text)
        for winner in blreg.find('div', class_ = "round-2 region-round").find_all('div', class_ = "team winner"):
            round2winners.append(winner.find('span', class_ = 'name').text)
        for winner in brreg.find('div', class_ = "round-2 region-round").find_all('div', class_ = "team winner"):
            round2winners.append(winner.find('span', class_ = 'name').text)
        ConvertTeamNames(round2winners)

        round3winners = [] #doubles as teams for round 4
        for winner in tlreg.find('div', class_ = "round-3 region-round").find_all('div', class_ = "team winner"):
            round3winners.append(winner.find('span', class_ = 'name').text)
        for winner in trreg.find('div', class_ = "round-3 region-round").find_all('div', class_ = "team winner"):
            round3winners.append(winner.find('span', class_ = 'name').text)
        for winner in blreg.find('div', class_ = "round-3 region-round").find_all('div', class_ = "team winner"):
            round3winners.append(winner.find('span', class_ = 'name').text)
        for winner in brreg.find('div', class_ = "round-3 region-round").find_all('div', class_ = "team winner"):
            round3winners.append(winner.find('span', class_ = 'name').text)
        ConvertTeamNames(round3winners)

        round4winners = [] #doubles as teams for final 4
        for winner in tlreg.find('div', class_ = "round-4 region-round").find_all('div', class_ = "team winner"):
            round4winners.append(winner.find('span', class_ = 'name').text)
        for winner in trreg.find('div', class_ = "round-4 region-round").find_all('div', class_ = "team winner"):
            round4winners.append(winner.find('span', class_ = 'name').text)
        for winner in blreg.find('div', class_ = "round-4 region-round").find_all('div', class_ = "team winner"):
            round4winners.append(winner.find('span', class_ = 'name').text)
        for winner in brreg.find('div', class_ = "round-4 region-round").find_all('div', class_ = "team winner"):
            round4winners.append(winner.find('span', class_ = 'name').text)
        ConvertTeamNames(round4winners)

        #----- Final 4 and Beyond -----#

        centerwinners = []
        for winner in soup.find('div', class_ = 'center-final-games').find_all('div', class_ = "team winner"):
            centerwinners.append(winner.find('span', class_ = 'name').text)

        champion = []
        champion.append(centerwinners.pop(1))

        #---------- Sports Reference Stats ----------#

        #----- Basic Team Stats -----#
        time.sleep(delay) #So the websites don't get ddosed lol
        link = requests.get(f'https://www.sports-reference.com/cbb/seasons/men/{year+1}-school-stats.html')
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

        if (len(notfoundteams) > 0): # don't continue if we don't have all the teams
            print(notfoundteams)
            raise ValueError("Error with team names inside loop. Stopping program.")
        
        #----- Basic Opponent Stats -----#
        time.sleep(delay) #So the websites don't get ddosed lol
        link = requests.get(f'https://www.sports-reference.com/cbb/seasons/men/{year+1}-opponent-stats.html')
        soup = BeautifulSoup(link.content, 'html.parser')
        schools = soup.find_all('td', attrs={"data-stat": "school_name"})
        osrrows = [] #sports reference rows
        notfoundteams = []
        for team in teams:
            found = False
            for school in schools:
                if school.find('a').text == team:
                    osrrows.append(school.find_parent('tr'))
                    found = True
            if not found:
                notfoundteams.append(team)

        CompareStats(teams, round1winners)
        CompareStats(round1winners, round2winners)
        CompareStats(round2winners, round3winners)
        CompareStats(round3winners, round4winners)
        CompareStats(round4winners, centerwinners)
        CompareStats(centerwinners, champion)
        print(f"{round((year-startyear+1)/(date.today().year-startyear), 2)*100}% trained...") #find a way to account for 2020?

    year += 1
print("100.0% trained!")
#---------- Training Model ----------#

if len(dataset) == 0:
    raise ValueError("Dataset is empty. Scraping likely failed.")

X = np.array([row[0] for row in dataset])
y = np.array([row[1] for row in dataset])

# Split BEFORE scaling (important!)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Fit scaler ONLY on training data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Results
print("Dataset size:", len(dataset))
print("Train Accuracy:", model.score(X_train, y_train))
print("Test Accuracy:", model.score(X_test, y_test))
print("Weights:", model.coef_)

#---------- Predict Current Tourney ----------#

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
ConvertTeamNames(teams)

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

if (len(notfoundteams) > 0): # don't continue if we don't have all the teams
    print(notfoundteams)
    raise ValueError("Error with team names outside loop. Stopping program.")

time.sleep(delay) #So the websites don't get ddosed lol
link = requests.get(f'https://www.sports-reference.com/cbb/seasons/men/{date.today().year}-opponent-stats.html')
soup = BeautifulSoup(link.content, 'html.parser')
schools = soup.find_all('td', attrs={"data-stat": "school_name"})
osrrows = [] #sports reference rows
notfoundteams = []
for team in teams:
    found = False
    for school in schools:
        if school.find('a').text == team:
            osrrows.append(school.find_parent('tr'))
            found = True
    if not found:
        notfoundteams.append(team)

if (len(notfoundteams) > 0): # don't continue if we don't have all the teams
    print(notfoundteams)
    raise ValueError("Error with team names outside loop. Stopping program.")

seeds = [1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,
        1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,
        1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,
        1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15
]

file = open(f"{path}/Data/Results.txt", "w")
while len(teams) != 1:
    teams, srrows, osrrows, seeds = PredictRound(teams, srrows, osrrows, seeds)
    # if (len(teams) == 4):
    #     print(seeds)
    #     print(teams)
    #     for row in srrows:
    #         print(row.find('a').text)
        # for orow in osrrows:
        #     print(orow.find('a').text)
file.close()
print("Prediction complete!")