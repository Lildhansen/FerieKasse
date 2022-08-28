#libraries - standard or pip
import codecs
from importlib.resources import path
import os
import orjson
import time
import configparser
from collections import OrderedDict

import sys #cmd args

#own modules
from menuStuff.Menu import Menu
import utilities.util as util
from classes.Player import Player
from Excel import Excel
import helperMain
import utilities.constants as const
import random
from classes.Email import Email

leagues = []
players = []
email = None

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
    print(folderName)
    if folderName == "" or folderName.isspace():
        return False
    if folderName[0] == "-":
        print("invalid name for a feriekasse")
        return False
    invalidSymbols = "/\\:*?\"<>|," #invalid symbols for a folder name + comma (as this is used for seperating multiple arguments)
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


def setupEmailIniFile():
    userInput = None
    while (userInput == None):
        userInput = util.parseIntOrNone(input("how often do you want to receive emails (in days) (0 = does not want to receive emails) "),0,365)
    if userInput == 0:
        return
    
    email = Email((os.path.join(os.path.dirname(__file__)),'Email.ini'))
    config = configparser.ConfigParser()
    try:
        config.add_section("email_config")
    except configparser.DuplicateSectionError:
        pass
    config.set("email_config", "sender", email.sender)
    config.set("email_config", "password", email.password)
    config.set("email_config", "server", email.server)
    config.set("email_config", "port", str(email.port))
    config.set("email_config", "initialEmailSent", "False")
    config.set("email_config", "emailInterval", str(userInput))

    
    #set language
    userInput = None
    while userInput != 1 and userInput != 2:
        userInput = util.parseIntOrNone(input("What language do you want the email to be in (1=Danish, 2=English) "))
    language = None
    if userInput == 1:
        language = "danish"
    elif userInput == 2:
        language = "english"
    config.set("email_config", "language", language)  
        
    #options for initial mail
    userInput = ""
    while userInput.lower() != "y" and userInput.lower() != "n":
        userInput = input("Do you want to input the receiving Emails and send the initial mail now (y/n) ")
    if userInput == "y":
        receivers = ""
        receiverInput = None
        print("write the emails to add seperated by enters (terminates on empty input) ")
        while receiverInput != "":
            receiverInput = input()
            receivers += receiverInput + ";"
        receivers = receivers.rstrip(";")
        config.set("email_config","receivers",receivers)
    else:  
        config.set("email_config", "receivers", "")
        print("ini file has been created, please add emails to receivers (seperated by semicolon) if you want to add automatic email service")
        print("You can then run make start start again to send initial email or just ignore the intial email.")
        
    with open(fr"data/{const.FERIEKASSE_NAME}/Email.ini", "w") as config_file:
        config.write(config_file)
#the main function of the file - sets up the feriekasse
def initiateFerieKasse():
    #opening prompts
    print("starting a new feriekasse")
    nameInput = ""
    while nameInput == "" or nameInput.lower() == "-l":
        nameInput = input("What name would you like to give the feriekasse? (n to cancel) (-l = list all feriekasser) ")
        if nameInput.lower() == "-l":
            helperMain.listAllFeriekasser()
    #checking/validating user input
    if nameInput == "n":
        print("cancelled")
        exit()
    if not folderIsValid(nameInput):
        print("invalid folder name")
        quit()
    const.FERIEKASSE_NAME = nameInput.strip()

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
    if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/extraRules.json"):
        setupExtraRulesFile()
    if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/Email.ini"):
        setupEmailIniFile()
    config = configparser.ConfigParser()
    config.read(fr"data/{const.FERIEKASSE_NAME}/Email.ini")
    email = Email(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__),"data"),const.FERIEKASSE_NAME),"email.ini"))
    if not util.parseBool(config.get("email_config","initialEmailSent")):
        email.sendInitialEmail()
        config.set("email_config","initialEmailSent","True")
        with open(fr"data/{const.FERIEKASSE_NAME}/Email.ini", "w") as config_file:
            config.write(config_file)
    print("succesfully updated all data of feriekasse:",const.FERIEKASSE_NAME)
    
if __name__ == "__main__":
    initiateFerieKasse()