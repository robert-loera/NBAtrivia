from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import teams
import json
import requests
import random
from random import randrange

#Function to return a random players playerID
def getPlayerID():
    nba_players = players.get_players()
    newPlayer = nba_players[randrange(len(nba_players))]
    playerID = newPlayer['id']
    return playerID

#Function to return json of common player info, needs to be passed playerID
#which will come from the getPlayerID() function
def getPlayerInfo(playerID):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id = playerID)
    custom_headers = {
        'Host': 'stats.nba.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    try:
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=playerID, proxy='http://127.0.0.1:80', headers=custom_headers, timeout=100)
    except (ConnectionError, requests.exceptions.ProxyError):
        pass
    pInfo = player_info.get_normalized_json()
    wjdata = json.loads(pInfo)
    return wjdata

def getMode(modes):
    mode = ""
    while mode not in modes:
        mode = input("Choose your trivia mode [%s]: " % ", ".join(modes))
    return mode

#Function to get the users input for which status mode the user would like to choose
def statusChoice(choices):
    choice = ""
    while choice not in choices:
        choice = input("Choose which type of players to be questioned on [%s]: " % ", ".join(choices))
    return choice

#Function to ask the user what city the team is from or in what year was the team founded
#will ask the user 15 questions ahnd return the score
def teamTrivia():
    nba_teams = teams.get_teams()
    y = random.sample(range(30), 15)
    score = 0
    for x in range(10):
        k = random.randint(0, 1)
        team = nba_teams[y[x]]['nickname']
        #if k==1 asl the user the year the organization was founded
        if k == 1:
            yrAnswer = (input("In what year was the " + str(team) + " organization founded: "))
            if yrAnswer == str(nba_teams[y[x]]["year_founded"]):
                score += 1
        #else ask user what city is the team from
        else:
            stAnswer = input("What city is the " + str(team) + " organization from: ")
            if stAnswer == nba_teams[y[x]]["city"]:
                score += 1
    return score

#Funtion to ask user which draft pick the player was, will return score
def draftTrivia(draftChoice):
    score = 0
    if draftChoice == "Inactive":
        x = 0
        #loop to search the data base and only ask draft question about inactive player
        while x != 10:
            pID = getPlayerID()
            pData = getPlayerInfo(pID)
            if pData["CommonPlayerInfo"][0]["ROSTERSTATUS"] == "Inactive":
                iAnswer = input("Which round was " + str(pData["CommonPlayerInfo"][0]["FIRST_NAME"]) +
                                " " + str(pData["CommonPlayerInfo"][0]["LAST_NAME"]) + " drafted: ")
                if iAnswer == str(pData["CommonPlayerInfo"][0]["DRAFT_ROUND"]):
                    score += 1
                x += 1
            else:
                pass
    if draftChoice == "Active":
        x = 0
        #loop to only ask about active players
        while x != 10:
            pID = getPlayerID()
            pData = getPlayerInfo(pID)
            if pData["CommonPlayerInfo"][0]["ROSTERSTATUS"] == "Active":
                iAnswer = input("Which round was " + str(pData["CommonPlayerInfo"][0]["FIRST_NAME"]) +
                                " " + str(pData["CommonPlayerInfo"][0]["LAST_NAME"]) + " drafted: ")
                if iAnswer == str(pData["CommonPlayerInfo"][0]["DRAFT_ROUND"]):
                    score += 1
                x += 1
            else:
                pass
    #will ask the user questions on all players no matter roster status
    if draftChoice == "Both":
        for x in range (10):
            pID = getPlayerID()
            pData = getPlayerInfo(pID)
            bAnswer = input("Which round was " + str(pData["CommonPlayerInfo"][0]["FIRST_NAME"]) +
                            " " + str(pData["CommonPlayerInfo"][0]["LAST_NAME"]) + " drafted: ")
            if bAnswer == str(pData["CommonPlayerInfo"][0]["DRAFT_ROUND"]):
                score += 1

    return score

#Function to ask the user 10 questions about what school a player went to and returns # of correct answeres (score
def schoolTrivia(schoolChoice):
    score = 0
    if schoolChoice == "Inactive":
        x = 0
        #loop to search the data base and only ask school question about inactive player
        while x != 10:
            pID = getPlayerID()
            pData = getPlayerInfo(pID)
            if pData["CommonPlayerInfo"][0]["ROSTERSTATUS"] == "Inactive":
                #print(pData["CommonPlayerInfo"][0]["SCHOOL"])
                iAnswer = input("What School was " + str(pData["CommonPlayerInfo"][0]["FIRST_NAME"]) +
                                " " + str(pData["CommonPlayerInfo"][0]["LAST_NAME"]) + " drafted from: ")
                if iAnswer == pData["CommonPlayerInfo"][0]["SCHOOL"]:
                    score += 1
                x += 1
            else:
                pass

    if schoolChoice == "Active":
        x = 0
        #loop to search the data base and only ask school question about active player
        while x != 10:
            pID = getPlayerID()
            pData = getPlayerInfo(pID)
            if pData["CommonPlayerInfo"][0]["ROSTERSTATUS"] == "Active":
                #print(pData["CommonPlayerInfo"][0]["SCHOOL"])
                aAnswer = input("What School was " + str(pData["CommonPlayerInfo"][0]["FIRST_NAME"]) +
                                " " + str(pData["CommonPlayerInfo"][0]["LAST_NAME"]) + " drafted from: ")
                if aAnswer == pData["CommonPlayerInfo"][0]["SCHOOL"]:
                    score += 1
                x += 1
            else:
                pass
    if schoolChoice == "Both":
        #loop to search the database and ask school questions no matter the roster status
        for x in range (10):
            pID = getPlayerID()
            pData = getPlayerInfo(pID)
            bAnswer = input("What School was " + str(pData["CommonPlayerInfo"][0]["FIRST_NAME"]) +
                            " " + str(pData["CommonPlayerInfo"][0]["LAST_NAME"]) + " drafted from: ")
            if bAnswer == pData["CommonPlayerInfo"][0]["SCHOOL"]:
                score += 1


    return score

#prompt the user for which trivia mode they would like to play
modes = getMode(["Team Trivia", "Draft Trivia", "School Trivia"])
if modes == "Team Trivia":
    score = teamTrivia()
    print("Your score is", score)

if modes == "Draft Trivia":
    draftChoice = statusChoice(["Inactive", "Active", "Both"])
    score = draftTrivia(draftChoice)
    print("Your score is", score)

if modes == "School Trivia":
    schoolChoice = statusChoice(["Inactive", "Active", "Both"])
    score = schoolTrivia(schoolChoice)
    print("Your score is", score)
