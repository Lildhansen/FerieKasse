#libraries - standard or pip
import codecs
from datetime import date
import json
from collections import namedtuple
import os
import configparser
import excel2img
from datetime import datetime


#own modules
from classes.Email import Email
from Excel import Excel
import utilities.util as util
import helperMain
import utilities.constants as const

#sets up the predefined links for each league
def setupLinks(leagues):
    for league in leagues:
        if league.name == "superliga":
            if datetime.now().month > 7:
                league.link = f"https://superstats.dk/program?aar={datetime.now().year}%2F{datetime.now().year+1}"
            else:
                league.link = f"https://superstats.dk/program?aar={datetime.now().year-1}%2F{datetime.now().year}"
        elif league.name == "premier-league":
            league.link = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
        elif league.name == "bundesliga":
            league.link = "https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures"
        elif league.name == "serie-a":
            league.link = "https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures"
        elif league.name == "laliga":
            league.link = "https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures"

#prompts the user for which feriekasse(r) to update - either a single one, multiple, all of them, or none of them (if it is cancelled)
#returns a list of the name of all the feriekasser to update
def loadFerieKasser():
    print("updating feriekasse ...")
    userInput = ""
    while userInput == "" or userInput.lower() == "-l": #todo: implement at man kan få skipped postponed matches
        userInput = input("Which feriekasse do you want to update? (if multiple - seperate each by comma) (n to cancel) (-a = all feriekasser) (-l = list all feriekasser) (' -sp' after a feriekasse name to skip postponed matches) (' -sp' after -a to skip postponed matches for all feriekasser): ")
        if userInput.lower() == "-l":
            helperMain.listAllFeriekasser()
    if userInput.lower().startswith("-a"):
        if " -sp" in userInput:
            userInput = handleSkipPostponedMatchesFlag(userInput)
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
        if not " -sp" in userInput:
            raise Exception("Feriekasser cannot contain '-' in their name. If this was intended to be a flag, please use '-sp' to skip postponed matches")
        userInput = handleSkipPostponedMatchesFlag(userInput)
    
    const.FERIEKASSE_NAME = userInput
    
    if not os.path.exists(fr"./data/{const.FERIEKASSE_NAME}"):
        raise Exception(f"feriekasse {const.FERIEKASSE_NAME} does not exist")
    return [const.FERIEKASSE_NAME]

def handleSkipPostponedMatchesFlag(userInput):
    const.SKIP_POSTPONED_MATCHES = True
    return userInput.removesuffix("-sp").strip() #if we remove the -sp flag and then strip the whitespace, we should get the feriekasse name, if input was valid
    

#removes the feriekasser without the proper data/files
def removeInvalidFeriekasserToRun(feriekasser):
    for feriekasse in feriekasser:
        if not os.path.exists(fr"./data/{feriekasse}/Feriekasse.xlsx"):
            feriekasser.remove(feriekasse)
        elif not os.path.exists(fr"./data/{feriekasse}/leaguesAndTeams.json"):
            feriekasser.remove(feriekasse)
        elif not os.path.exists(fr"./data/{feriekasse}/latestMatchCovered.json"):
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
    
#Gets the latest match covered for a specific league from the latest match covered JSON file, and returns that match as a Match object
def getLatestMatchCovered(league):
    file = codecs.open(fr"./data/{const.FERIEKASSE_NAME}/latestMatchCovered.json","r")
    fileJson = json.loads(file.read())
    fileDict = fileJson[f"{league.name},{league.country}"]
    if fileDict == {} or fileDict == None: #if no latest match was covered - ie it is the first time we run main_update
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
    
    return (date.today() - lastSentMailDate).days >= const.SEND_MAIL_INTERVAL_DAYS

#sends the periodic mail using the Email object, and afterwards updates the last mail sent value of the .ini file 
def sendPeriodicMail(players):
    email = Email(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__),"data"),const.FERIEKASSE_NAME),"Email.ini"))
    email.sendPeriodicMail(players)
    email.updateLastMailSentValue(fr"data/{const.FERIEKASSE_NAME}/email.ini")

#updates the latestMatchCovered file by replacing it with the one altered by the leagues when running the application
def updateLatestMatchCovered():
    oldLatestMatchCovered = os.path.join("data", const.FERIEKASSE_NAME, "latestMatchCovered.json")
    newLatestMatchCovered = os.path.join("data", const.FERIEKASSE_NAME, "latestMatchCoveredToUpdate.json")

    
    
    # Remove the existing latestMatchCovered.json file
    if os.path.exists(oldLatestMatchCovered):
        os.remove(oldLatestMatchCovered)
    
    # Rename latestMatchCoveredToUpdate.json to latestMatchCovered.json
    os.rename(newLatestMatchCovered, oldLatestMatchCovered)
    

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
        setupLinks(leagues)
        players = util.getPlayerObjectsFromFile()
        for league in leagues:
            print("working on",league.name)
            match = getLatestMatchCovered(league)
            if league.name == "superliga": #special case for superliga, as the site does not support results for superliga anymore
                # continue
                if match == None:
                    league.getMatchesAfterLatestMatchForSuperliga()
                else:
                    league.getMatchesAfterLatestMatchForSuperliga(match)
            else:
                if match == None:
                    league.getMatchesAfterLatestMatch()
                else:
                    league.getMatchesAfterLatestMatch(match)
            league.calculatePointsForMatches()
            league.removeMatchesYielding0Points()
            for match in league.matches:
                assignMatchToPlayers(match,players)
        myExcel = Excel(leagues)
        myExcel.updateExcelFile(players)
        if mailShouldBeSent():
            sendPeriodicMail(players)
        updateLatestMatchCovered()
        
if __name__ == "__main__":
    UpdateFerieKasse()