from datetime import date, timedelta, datetime
import re
from xml.dom.minidom import Element
import orjson
import codecs

from classes.Match import Match
from classes.Player import Player

#consts
INVALID_LETTERS = "æøå"

#parses input into an int if possible - otherwise returns None (rather than throwing an exception)
def parseIntOrNone(input,minValue=0,maxValue=0):
    output = None
    try:
        output = int(input)
    except ValueError:
        return None
    if minValue != 0 or maxValue != 0:
        if output > maxValue or output < minValue:
            return None
    return output

#.txt files have issues reading æøå so these are simply removed when used for comparison and URL generation fx
def removeInvalidLetters(myStr):
    for letter in INVALID_LETTERS:
        if (letter in myStr.lower()):
            myStr = myStr.replace(letter,"")
    return myStr
        
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


def splitAndConvertToInt(inputString,seperator):
    result = []
    splittedList = inputString.split(seperator)
    for element in splittedList:
        result.append(int(element))
    return result

#expects input in the form 2021-08-14
def textToDate(text):
    year,month,day = splitAndConvertToInt(text,"-")
    return date(year,month,day)
    
#converts named tuple, match, into a match object and returns it - will only be called if not None
def matchTupleToMatchObject(matchTuple):
    return Match(textToDate(matchTuple.date),matchTuple.homeTeam,matchTuple.homeGoals,matchTuple.awayTeam,matchTuple.awayGoals)
    
def getPlayerObjectsFromFile():
    players = []
    file = codecs.open(r"./logs/leaguesAndTeams.json","r",encoding='UTF-8')
    jsonData = orjson.loads(file.read())
    for leagueAndCountry in jsonData:
        for teamName in jsonData[leagueAndCountry]:
            teamName = teamName
            playerName = jsonData[leagueAndCountry][teamName]
            player = findPlayerObjectInPlayerListFromPlayerName(playerName,players)
            if player == None:
                player = Player(playerName)
                player.teams.append(teamName)
                players.append(player)
            else:
                player.teams.append(teamName)
    return players

def findPlayerObjectInPlayerListFromPlayerName(playerName,players):
    for player in players:
        if playerName == player.name:
            return player
        else:
            continue
    return None
    
    