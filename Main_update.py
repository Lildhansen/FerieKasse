#libraries - standard or pip
import codecs
from datetime import date
import json
from collections import namedtuple
import os


#own modules
from classes.Email import Email
from Excel import Excel
import utilities.util as util
import helperMain
import utilities.constants as const

def setupLinks(leagues):
    for league in leagues:
        if league.name == "superliga":
            league.link = "https://fbref.com/en/comps/50/schedule/Superliga-Scores-and-Fixtures"
        elif league.name == "premier-league":
            league.link = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
        elif league.name == "bundesliga":
            league.link = "https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures"
        elif league.name == "serie-a":
            league.link = "https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures"
        elif league.name == "laliga":
            league.link = "https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures"
def loadFerieKasse():
    print("updating feriekasse ...")
    const.FERIEKASSE_NAME = input("Which feriekasse do you want to update? (n to cancel) ")
    if const.FERIEKASSE_NAME == "n":
        print("cancelled")
        exit()
    if not os.path.exists(fr"./data/{const.FERIEKASSE_NAME}"):
        print("This feriekasse does not exist")
        exit()
    if os.path.exists(fr"data/{const.FERIEKASSE_NAME}/extraRules.json"):
        const.FOUR_GOAL_WIN_RULE = True
        

def UpdateFerieKasse():
    loadFerieKasse()
    leagues = helperMain.getAllLeagues()
    setupLinks(leagues)
    players = util.getPlayerObjectsFromFile()
    for league in leagues:
        print("working on",league.name)
        match = getLatestMatchCovered(league)
        if match == None:
            league.getMatchesAfterLatestMatch()
        else:
            league.getMatchesAfterLatestMatch(match)
        league.calculatePointsForMatches(players)
        league.removeMatchesYielding0Points()
        for match in league.matches:
            assignMatchToPlayers(match,players)
    addToLastEditedFile()
    myExcel = Excel(leagues)
    myExcel.updateExcelFile(players)
    if mailShouldBeSent():
        sendPeriodicMail()
    
def addToLastEditedFile():
    with open("./data/teams.json","w") as file:
        file.write(date.today().isoformat())

def getLatestMatchCovered(league):
    file = codecs.open(fr"./data/{const.FERIEKASSE_NAME}/latestMatchCovered.json","r")
    fileJson = json.loads(file.read())
    fileDict = fileJson[f"{league.name},{league.country}"]
    if fileDict == {}: #if no latest match was covered - ie it is the first time we run main_update
        return None
    match = json.loads(fileDict)
    matchJson = json.dumps(match)
    matchTuple = json.loads(matchJson, object_hook = lambda d : namedtuple('Match', d.keys())(*d.values()))
    file.close()
    return util.matchTupleToMatchObject(matchTuple)

#assigns a specific match to a player depending on if one of the player's team is in the match (will only assign match to player if the player loses point for that match)
#can be assigned to 2 players, if it is a draw with 2 different players' teams
def assignMatchToPlayers(match,players):
    homePlayer, awayPlayer = None,None
    if match.homeTeamIsPlayerTeam:
        homePlayer = util.getPlayerThatHasTeam(match.homeTeam,players)
    if match.awayTeamIsPlayerTeam:
        awayPlayer = util.getPlayerThatHasTeam(match.awayTeam,players)
    if match.homeTeamIsWinner or match.draw:
        tryAppendMatch(awayPlayer,match)
    if not match.homeTeamIsWinner or match.draw:
        tryAppendMatch(homePlayer,match)

def tryAppendMatch(player,match):
    if player == None:
        return
    player.matches.append(match)
    
def mailShouldBeSent():
    with open(fr"data/{const.FERIEKASSE_NAME}/lastEdited.txt","r") as file:
        dateLastEdited = util.textToDate(file.read())
    return (date.today() - dateLastEdited).days >= const.SEND_MAIL_INTERVAL_DAYS
        
    #læs fra lastEdited.txt og check dato med dagens dato (og se om der er gået x dage siden) - hvor x er hvor ofte vi skal sende mails     
    #returner true eller false
    
def sendPeriodicMail():
    email = Email(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__),"data"),const.FERIEKASSE_NAME),"email.ini"))
    email.sendPeriodicMail()
    #brug Email class
    
if __name__ == "__main__":
    UpdateFerieKasse()
