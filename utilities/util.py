from datetime import date
import datetime
import orjson
import codecs
import math

from classes.Match import Match
from classes.Player import Player
from classes.Team import Team
import utilities.constants as const

#function that return false if folder is invalid (that is consists of any of the invalid chars or does not comply with predefined rules) and true otherwise
def folderIsValid(folderName):
    if folderName == "" or folderName.isspace():
        return False
    invalidSymbols = "/\\:*?\"<>|,-" #invalid symbols for a folder name + comma (as this is used for seperating multiple arguments) + dash (used for flags)
    for invalidSymbol in invalidSymbols:
        if invalidSymbol in folderName:
            return False
    return True

#parses input into an int if possible - otherwise returns None (rather than throwing an exception)
def parseIntOrNone(input,minValue=0,maxValue=math.inf):
    output = None
    try:
        output = int(input)
    except ValueError:
        return None
    if minValue != 0 or maxValue != math.inf:
        if output > maxValue or output < minValue:
            return None
    return output

#returns True if "1", 1, or "True", otherwise ALWAYS False
def parseBool(input):
    if input == None:
        return False
    if input == "True" or parseIntOrNone(input) == 1:
        return True
    else:
        return False
#parses input into a float if possible - otherwise returns None (rather than throwing an exception)
def parseFloatOrNone(input,minValue=0,maxValue=math.inf):
    output = None
    try:
        output = float(input)
    except ValueError:
        return None
    if minValue != 0 or maxValue != math.inf:
        if output > maxValue or output < minValue:
            return None
    return output
        
#for excelfile
#number is always at least 1
#max working output = ZZ
def numberToExcelColumn(number):
    result = ""
    chars = " ABCDEFGHIJKLMNOPQRSTUVWXYZ" #first blank space is intended
    while number > len(chars)-1:
        if result != "":
            nextLetterIndex = chars.index(result[-1])+1
            if nextLetterIndex == len(chars):
                nextLetterIndex = 1
            result = result[1:-1] + chars[nextLetterIndex]
            number -= len(chars)-1
        else:
            result += chars[1]
            number -= len(chars)-1
    if (number != 0):
        result += chars[number]
    return result

#gets the sum of an excel cell like: "=1+2+3+4+5"
def getSumOfExcelCell(cell):
    cell = cell.strip("=")
    numbersInCell = cell.split("+")
    sum = 0
    for number in numbersInCell:
        sum += int(float(number))
    return sum

#does the same as split, but converts the parts to ints and finally returns a list (which can be unpacked as a tuple) of the parts
def splitAndConvertToInt(inputString,seperator):
    result = []
    splittedList = inputString.split(seperator)
    for element in splittedList:
        result.append(parseIntOrNone(element))
    return result

#expects input in the form 2021-08-14
def textToDate(text):
    year,month,day = splitAndConvertToInt(text,"-")
    return date(year,month,day)

#expects input in the form 03/09 14.00
def dateAndTimeToDate(dateAndTime):
    dateAndTime = dateAndTime.strip()
    rawDate = dateAndTime.split(" ")[0]
    day, month = map(int, rawDate.split("/"))
    if datetime.datetime.now().month > 7: #if we are in the first half of the season, all matches are from this year
        year = datetime.datetime.now().year
    else: #if we are in the final half of the season
        if month > 7: #if the match is in the first half of the season, it is from last year
            year = datetime.datetime.now().year-1
        else: #if the match is in the final half of the season, it is from this year
            year = datetime.datetime.now().year
    return date(year,month,day)
        
#input = teams in 2/3 letter format
def extractSuperligaTeams(shortTeamName):
    translator = {
        "BIF": "Brøndby",
        "FCM": "Midtjylland",
        "FCK": "FC Copenhagen",
        "FCN": "Nordsjælland",
        "AGF": "AGF",
        "SIF": "Silkeborg",
        "RFC": "Randers",
        "VFF": "Viborg",
        "OB": "Odense",
        "LBK": "Lyngby",
        "VB": "Vejle BK",
        "HIF": "Hvidovre IF",
    }
    if shortTeamName not in translator:
        raise ValueError(f"Unknown team: {shortTeamName}")
    return translator[shortTeamName]


#converts named tuple, match, into a match object and returns it - will only be called if not None
def matchTupleToMatchObject(matchTuple):
    return Match(textToDate(matchTuple.date),matchTuple.homeTeam,matchTuple.homeGoals,matchTuple.awayTeam,matchTuple.awayGoals)

#find team in list of teams based one team name
def findTeamByTeamName(teams,teamName):
    for team in teams:
        if team.name.lower() == teamName.lower():
            return team
    raise Exception("team not found")

#gets all players from leaguesAndTeams.json and make a Player object for each of them and finally returns a list of them
def getPlayerObjectsFromFile():
    players = []
    file = codecs.open(fr"./data/{const.FERIEKASSE_NAME}/leaguesAndTeams.json","r",encoding='UTF-8')
    jsonData = orjson.loads(file.read())
    for leagueAndCountry in jsonData:
        leagueName = leagueAndCountry.split(",")[0]
        for teamName in jsonData[leagueAndCountry]:
            teamName = teamName
            playerName = jsonData[leagueAndCountry][teamName]
            player = findPlayerObjectInPlayerListFromPlayerName(playerName,players)
            if player == None:
                player = Player(playerName)
                player.teams.append(Team(teamName,player.name,leagueName))
                players.append(player)
            else:
                player.teams.append(Team(teamName,player.name,leagueName))
    return players

#returns the player that has the team with the given name from a list of players 
#the teams of each player must be strings rather than team objects
def getPlayerThatHasTeam(teamName,players):
    for player in players:
        for team in player.teams:
            if team.name == teamName:
                return player
    return None

def findPlayerObjectInPlayerListFromPlayerName(playerName,players):
    for player in players:
        if playerName == player.name:
            return player
        else:
            continue
    return None


    