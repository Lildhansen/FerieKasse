#libraries - standard or pip
import codecs
from importlib.resources import path
import os
import orjson
import time
import configparser

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
#email = Email((os.path.join(os.path.dirname(__file__)),'Email.ini'))
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
    userInput = ""
    while userInput != "0" and userInput != "1":
        userInput = input("would you like to add extra rules? (0=no) (1=gain points for 4 goal win) ")
    if userInput == "0":
        return
    with open(fr"data/{const.FERIEKASSE_NAME}/extraRules.json","wb") as file:
        file.write(orjson.dumps({"4GoalWinRule":True}))

def setupLastEditedFile():
    with open(fr"data/{const.FERIEKASSE_NAME}/lastEdited.txt","w") as _:
        pass

def setupEmailIniFile():
    email = Email(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__),"data"),const.FERIEKASSE_NAME),"email.ini"))
    print(email)
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

    userInput = ""
    while userInput.lower() != "y" and userInput.lower() != "n":
        userInput = input("Do you want to input the receiving Emails and send the initial mail now (y/n) ")
    if userInput == "y":
        receivers = ""
        receiverInput = None
        print("write the emails to add seperated by enters (terminates on empty input)")
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
    #completes the setup if the user has added the folder and then added the leaguesAndTeams.json file themself
    if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx"):
        myExcel = Excel(leagues)
        myExcel.setupExcelFile()
    if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/latestMatchCovered.json"):
        setupLatestMatchCoveredForEachLeagueFile()
    if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/extraRules.json"):
        setupExtraRulesFile()
    if not os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/lastEdited.txt"):
        setupLastEditedFile()
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