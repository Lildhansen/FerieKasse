#libraries - standard or pip
import codecs
import datetime
import json
import orjson
from collections import namedtuple
import os
import configparser
import excel2img


#own modules
from classes.Email import Email
from Excel import Excel
import utilities.util as util
import helperMain
import utilities.constants as const

#prompts the user for which feriekasse(r) to update - either a single one, multiple, all of them, or none of them (if it is cancelled)
#returns a list of the name of all the feriekasser to update
def loadFerieKasser():
    print("updating feriekasse ...")
    userInput = ""
    while userInput == "" or userInput.lower() == "-l": #todo: implement at man kan få skipped postponed matches
        userInput = input("Which feriekasse do you want to update? (if multiple - seperate each by comma) (n to cancel) (-a = all feriekasser) (-l = list all feriekasser)")
        if userInput.lower() == "-l":
            helperMain.listAllFeriekasser()
    if userInput.lower().startswith("-a"):
        if userInput.lower() != "-a":
            raise Exception("if inputting '-a', no other text than ' -sp' is allowed as well")
        feriekasser = []
        for feriekasse in os.listdir("data"):
            feriekasseDirectory = os.path.join("data", feriekasse)
            if os.path.isdir(feriekasseDirectory):
                if (feriekasse == "unitTests"):
                    continue
                feriekasser.append(feriekasse)
        return feriekasser  
    elif userInput.lower()[0] == "-":
        print("invalid flag entered")
        quit()
    elif "," in userInput:
        return helperMain.handleMultipleArgumentsForFeriekasser(userInput)

    
    if userInput.lower() == "n":
        print("cancelled")
        quit()
    
    if "-" in userInput:
        raise Exception("Feriekasser cannot contain '-' in their name. If this was intended to be a flag, please use '-sp' to skip postponed matches")

    if "test" in userInput.lower():
        raise Exception("Feriekasser cannot contain the word 'test' in their name")
    
    const.FERIEKASSE_NAME = userInput
    
    if not os.path.exists(fr"./data/{const.FERIEKASSE_NAME}"):
        raise Exception(f"feriekasse {const.FERIEKASSE_NAME} does not exist")
    return [const.FERIEKASSE_NAME]

#removes the feriekasser without the proper data/files
def removeInvalidFeriekasserToRun(feriekasser):
    for feriekasse in feriekasser:
        if not os.path.exists(fr"./data/{feriekasse}/Feriekasse.xlsx"):
            feriekasser.remove(feriekasse)
        elif not os.path.exists(fr"./data/{feriekasse}/leaguesAndTeams.json"):
            feriekasser.remove(feriekasse)
        elif not os.path.exists(fr"./data/{feriekasse}/latestDateCovered.txt"):
            feriekasser.remove(feriekasse)
        #more checks?



#sets the extra rules of the feriekasse by reading from the extra rules JSON file and then setting the constant values
def configureExtraRules():
    with open(fr"data/{const.FERIEKASSE_NAME}/extraRules.json","r") as file:
        extraRules = json.loads(file.read())
        for constant,value in extraRules.items():
            setConstant(constant,value)

#sets the constant value to the value inputted, the constant value to change is based on a string of the name of the constant
def setConstant(constantString,value):
    if constantString == "DRAW_POINTS":
        const.DRAW_POINTS = value
    elif constantString == "LOSE_POINTS":
        const.LOSE_POINTS = value
    elif constantString == "POINTS_PER_GOAL":
        const.POINTS_PER_GOAL = value
    elif constantString == "INDBYRDES_MULTIPLIER":
        const.INDBYRDES_MULTIPLIER = value
    elif constantString == "EXTRA_TEAMS_PER_PLAYER":
        const.EXTRA_TEAMS_PER_PLAYER = value
    elif constantString == "TEAMS_PER_PLAYER":
        const.TEAMS_PER_PLAYER = value
    elif constantString == "FOUR_GOAL_WIN_BONUS_POINTS":
        const.FOUR_GOAL_WIN_BONUS_POINTS = value
    elif constantString == "FOUR_GOAL_WIN_RULE":
        const.FOUR_GOAL_WIN_RULE = value
    else:
        raise Exception(f"the constant {constantString} not found")

def getLatestDateCovered():
    path = fr"./data/{const.FERIEKASSE_NAME}/latestDateCovered.txt"
    if not os.path.exists(path):
        return None
    with open(path,"r") as file:
        dateText = file.read().strip()
        if dateText == "":
            return None
        return util.textToDate(dateText)
    

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
    if const.FOUR_GOAL_WIN_BONUS_POINTS:
        if match.bonusPoints != 0:

            if match.homeTeamIsWinner:
                tryAppendMatch(homePlayer,match)
            else:
                tryAppendMatch(awayPlayer,match) 
      
        
  
#appends match to player's matches, except if player is None, then nothing happens
def tryAppendMatch(player,match):
    if player == None:
        return
    player.matches.append(match)

#returns true if a mail should be sent - that is if an Email.ini exists and that there has passed enough days since the last sent mail
def mailShouldBeSent():
    if not os.path.exists(fr"data/{const.FERIEKASSE_NAME}/Email.ini"):
        return False
    lastSentMailDate = None
    with open(fr"data/{const.FERIEKASSE_NAME}/Email.ini","r") as file:
        config = configparser.ConfigParser()
        config.read_file(file)
        try:
            lastSentMailDate = util.textToDate(config.get("email_config","lastdatesent"))
        except configparser.NoOptionError:
            return True #if no last sent mail date is found, send mail always
        const.SEND_MAIL_INTERVAL_DAYS = int(config.get("email_config","emailInterval"))
    
    return (datetime.date.today() - lastSentMailDate).days >= const.SEND_MAIL_INTERVAL_DAYS

#sends the periodic mail using the Email object, and afterwards updates the last mail sent value of the .ini file 
def sendPeriodicMail(players):
    email = Email(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__),"data"),const.FERIEKASSE_NAME),"Email.ini"))
    email.sendPeriodicMail(players)
    email.updateLastMailSentValue(fr"data/{const.FERIEKASSE_NAME}/email.ini")

def updateLatestDateCovered(date):
    with open(fr"./data/{const.FERIEKASSE_NAME}/latestDateCovered.txt","w") as file:
        file.write(date.strftime("%Y-%m-%d"))
    

#the main function of the file - updates an or multiple feriekasser
def UpdateFerieKasse():
    feriekasser = loadFerieKasser()
    removeInvalidFeriekasserToRun(feriekasser)
    if (feriekasser == []):
        print("selected feriekasser cannot be run")
        quit()
    if os.path.exists(fr"data/{const.FERIEKASSE_NAME}/extraRules.json"):
        configureExtraRules()
    for feriekasse in feriekasser: #usually just one, but with the -a flag we run multiple feriekasser
        print(f"running feriekasse, {feriekasse}")
        const.FERIEKASSE_NAME = feriekasse
        leagues = helperMain.getAllLeagues()
        players = util.getPlayerObjectsFromFile()
        latestDateCovered = getLatestDateCovered()
        latestDateToCover = datetime.date.today() - datetime.timedelta(days=1) #yesterday
        # latestDateToCover = datetime.date(2025,10,27) #for testing purposes
        for league in leagues:
            print("working on",league.name)
            if latestDateCovered == None:
                league.getMatchesBetweenDates(fromDate=None,toDate=latestDateToCover)
            else:
                #look at the latest date covered + 1 day forward up to latest date to cover (ie yesterday)
                league.getMatchesBetweenDates(latestDateCovered + datetime.timedelta(days=1), latestDateToCover) 
            league.calculatePointsForMatches()
            league.removeMatchesYielding0Points()
            for match in league.matches:
                assignMatchToPlayers(match,players)
        myExcel = Excel(leagues)
        myExcel.updateExcelFile(players)
        if mailShouldBeSent():
            sendPeriodicMail(players)
        updateLatestDateCovered(latestDateToCover)

        
if __name__ == "__main__":
    UpdateFerieKasse()