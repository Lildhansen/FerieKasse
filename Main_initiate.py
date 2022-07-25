#libraries - standard or pip
import codecs
import os
import orjson
import time
from collections import OrderedDict

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

#function that return false if folder is invalid (that is consists of any of the invalid chars or does not comply with predefined rules) and true otherwise
def folderIsValid(folderName):
    if const.FERIEKASSE_NAME == "" or const.FERIEKASSE_NAME.isspace():
        return False
    if const.FERIEKASSE_NAME == "all":
        print("invalid name for a feriekasse")
        return False
    invalidSymbols = "/\\:*?\"<>|"
    for invalidSymbol in invalidSymbols:
        if invalidSymbol in folderName:
            return False
    return True
        
def setupExtraRulesFile():
    extraRulesDictionary = {}
    userInput = ""
    
    #change constants
    while userInput != "n" and userInput != "y":
        userInput = input("would you like to the change the constant values for points (y/n) ").lower()
    if userInput == "y":
        const.LOSE_POINTS = getConstValue("Points for loss ")
        const.DRAW_POINTS = getConstValue("Points for draw ")
        const.POINTS_PER_GOAL = getConstValue("Points per goal ")
        const.INDBYRDES_MULTIPLIER = getConstValue("Multiplier for indbyrdes matches ",float)
        const.EXTRA_TEAMS_PER_PLAYER = getConstValue("Number of extra teams per player (where all leagues are available) ")
        const.TEAMS_PER_PLAYER = getConstValue("Number of teams per player (including extra teams) ",minValue=const.EXTRA_TEAMS_PER_PLAYER)
        extraRulesDictionary = {"LOSE_POINTS":const.LOSE_POINTS,"DRAW_POINTS":const.DRAW_POINTS,"POINTS_PER_GOAL":const.POINTS_PER_GOAL,"INDBYRDES_MULTIPLIER":const.INDBYRDES_MULTIPLIER,"EXTRA_TEAMS_PER_PLAYER":const.EXTRA_TEAMS_PER_PLAYER,"TEAMS_PER_PLAYER":const.TEAMS_PER_PLAYER}
    
    #new rules
    userInput = ""
    while userInput != "n" and userInput != "y":
        userInput = input("would you like to the add the rule where you lose points (earn money) with at least a 4 goal win (y/n) ").lower()
    if userInput == "y":
        const.FOUR_GOAL_WIN_BONUS_POINTS = - abs(getConstValue("number of points for 4 goal win ")) #will always be negative
        extraRulesDictionary["FOUR_GOAL_WIN_RULE"] = True
        extraRulesDictionary["FOUR_GOAL_WIN_BONUS_POINTS"] = const.FOUR_GOAL_WIN_BONUS_POINTS
    with open(fr"data/{const.FERIEKASSE_NAME}/extraRules.json","wb") as file:
        file.write(orjson.dumps(extraRulesDictionary))

def getConstValue(prompt,type=int,minValue=0):
    value = None
    while not isinstance(value,type) or value < minValue:
        if type == float:
            value = util.parseFloatOrNone(input(prompt),minValue)
        elif type == int:
            value = util.parseIntOrNone(input(prompt),minValue)
        else:
            raise Exception(f"type must be int or float, not {type}")
    return value

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
    #if the folder already exist - the user is either mid game or havent filled out all information
    if os.path.exists(newDir):
        print("a feriekasse with this name already exists")
        print("updates data if all is not present")
        leagues = helperMain.getAllLeagues()
    #if folder doesnt exist we are starting a completely new game
    else:
        os.mkdir(newDir)
        if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/extraRules.json"):
            setupExtraRulesFile()
        file = fr"{newDir}/leaguesAndTeams.json"
        if not (os.path.isfile(file) and os.path.getsize(file) > 0):
            setupMenuInitiation()
            print("teams have been loaded into the feriekasse")
            time.sleep(2)
        leagues = helperMain.getAllLeagues()
        myExcel = Excel(leagues)
        myExcel.setupExcelFile()
        setupLatestMatchCoveredForEachLeagueFile()
        print("successfully started feriekasse:",const.FERIEKASSE_NAME)
    #completes the setup if the user has added the folder themselves - and then added the leaguesAndTeams.json file
    if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/extraRules.json"):
        setupExtraRulesFile()
    if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx"):
        myExcel = Excel(leagues)
        myExcel.setupExcelFile()
    if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/latestMatchCovered.json"):
        setupLatestMatchCoveredForEachLeagueFile()
    print("succesfully updated all data of feriekasse:",const.FERIEKASSE_NAME)
    
if __name__ == "__main__":
    initiateFerieKasse()