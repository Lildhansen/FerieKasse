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

#function that return false if folder is invalid (that is consists of any of the invalid chars) and true otherwise
def folderIsValid(folderName):
    if const.FERIEKASSE_NAME == "" or const.FERIEKASSE_NAME.isspace():
        return False
    invalidSymbols = "/\\:*?\"<>|"
    for invalidSymbol in invalidSymbols:
        if invalidSymbol in folderName:
            return False
    return True
        
    

#the main function of the file - sets up the feriekasse
def initiateFerieKasse():
    #opening prompts
    print("starting a new feriekasse")
    const.FERIEKASSE_NAME = input("What name would you like to give the feriekasse? (n to cancel) ")
    #checking/validating user input
    if const.FERIEKASSE_NAME == "n":
        print("cancelled")
        exit()
    if not folderIsValid(const.FERIEKASSE_NAME):
        print("invalid folder name")
        quit()

    newDir = fr"./data/{const.FERIEKASSE_NAME}"
    helperMain.getAllLeagues()
    #if the folder already exist - the user is either mid game or havent filled out all information
    if os.path.exists(newDir):
        print("a feriekasse with this name already exists")
        print("updates data if all is not present")
    #if folder doesnt exist we are starting a completely new game
    else:
        os.mkdir(newDir)
        file = fr"{newDir}/leaguesAndTeams.json"
        if not (os.path.isfile(file) and os.path.getsize(file) > 0):
            setupMenuInitiation()
        myExcel = Excel(leagues)
        myExcel.setupExcelFile()
        setupLatestMatchCoveredForEachLeagueFile()
        print("successfully started feriekasse",const.FERIEKASSE_NAME)
        quit()
    #completes the setup if the user has added the folder themselves - and then added the leaguesAndTeams.json file
    if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx"):
        myExcel = Excel(leagues)
        myExcel.setupExcelFile()
    if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/latestMatchCovered.json"):
        setupLatestMatchCoveredForEachLeagueFile()
    print("succesfully updated all data of feriekasse",const.FERIEKASSE_NAME)
    
if __name__ == "__main__":
    initiateFerieKasse()