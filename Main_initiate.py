#libraries - standard or pip
import codecs
import os
import orjson

#own modules
from menuStuff.Menu import Menu
import utilities.util as util
from classes.Player import Player
from Excel import Excel
import helperMain
import utilities.constants as const
import random


leagues = []
players = []

#terminal prompting the user the selection of players, then initiating the menu for selecting teams
def setupMenuInitiation():
    numOfPlayers = ""
    while (util.parseIntOrNone(numOfPlayers,1,8) == None):
        numOfPlayers = input("number of players: ")
    numOfPlayers = int(numOfPlayers)
    print(f"write the {numOfPlayers} players (seperated by enter):")
    while len(players) < numOfPlayers:
        playerName = input()
        if playerName == "" or playerName.isspace():
            continue
        players.append(Player(playerName))
    random.shuffle(players)
    myMenu = Menu(players,"Select a league/country")
    myMenu.setupMenu()
    myMenu.run()
    myMenu.saveInJson()

#orjson
def setupLatestMatchCoveredForEachLeagueFile():
    with codecs.open(fr"./data/{const.FERIEKASSE_NAME}/latestMatchCovered.json","wb") as file:
        file.write(orjson.dumps(const.LeagueNationsDict))

#the main function of the file - sets up the feriekasse
def initiateFerieKasse():
    print("starting a new feriekasse")
    const.FERIEKASSE_NAME = input("What name would you like to give the feriekasse? (n to cancel) ")
    if const.FERIEKASSE_NAME == "n":
        print("canceled")
        exit()
    newDir = fr"./data/{const.FERIEKASSE_NAME}"
    if os.path.exists(newDir):
        print("a feriekasse with this name already exists")
        exit()
    os.mkdir(newDir)
    file = fr"{newDir}/leaguesAndTeams.json"
    if not (os.path.isfile(file) and os.path.getsize(file) > 0):
        setupMenuInitiation()
    helperMain.getAllLeagues()
    myExcel = Excel(leagues)
    myExcel.setupExcelFile()
    setupLatestMatchCoveredForEachLeagueFile()
    print("successfully started feriekasse",const.FERIEKASSE_NAME)
    
if __name__ == "__main__":
    initiateFerieKasse()