#libraries - standard or pip
from datetime import date
import time
import bs4
import urllib.request
from urllib.error import HTTPError, URLError
import re

#own libraries
from classes.Match import Match
import utilities.util as util
import utilities.constants as const

class Soup:
    def __init__(self):
        self.res = None
        self.soup = None

    #gets the content of the links and saves it in self.soup
    def getLinkContent(self,link):
        time.sleep(1)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        req = urllib.request.Request(link, headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                self.res = response.read()
                self.soup = bs4.BeautifulSoup(self.res, "html.parser")
        except HTTPError as e:
            print(f'HTTPError: {e.code} for url: {link}')
        except URLError as e:
            print(f'URLError: {e.reason} for url: {link}')
        except Exception as e:
            print(f'Unexpected error: {e}')

    #takes the latest match that has been processed as input, and get all matches in that specific league between that match+1 and the last played match
    def getMatchesAfterLatestMatch(self,latestMatch):
        allMatches = []
        body = self.soup.find('tbody')
        #this consists of a mix of matches and filler rows in the table (like headers) 
        elementsInBody = body.find_all(recursive=False) # i think this works now
        for rawMatch in elementsInBody:
            if len(rawMatch.text) == 0 or rawMatch.text == None:
                continue
            currentMatch = self.rawMatchToMatchObject(rawMatch)
            if currentMatch.date <= latestMatch.date: #if we have already looked at this match earlier
                continue
            #not sure which one it is, but if it has no score, it is in progress or havent been played (and from there on the rest of the matches are the same (except if they have been postponed))
            elif currentMatch.homeGoals == None or currentMatch.homeGoals == "": 
                #Although we do not know if it is a postponed match yet, 
                # we know that it should break in all circumstances if we are not skipping postponed matches
                if not const.SKIP_POSTPONED_MATCHES: 
                    break
                if self.matchIsPostponed(rawMatch):
                    continue
                else:
                    break
            elif currentMatch.date == date.today(): #if it is today, we don't check it 
                continue
            allMatches.append(currentMatch)
        return allMatches
    
    def getMatchesAfterLatestMatchForSuperliga(self,latestMatch):
        allMatches = []
        allRounds = self.soup.find_all('div',class_="box full blue multipleheader")
        for round in allRounds:
            if round.find('tbody') == None:
                continue
            round = round.find('tbody')
            pattern = re.compile(r"<tr>.*?/>", re.DOTALL)
            matches = pattern.findall(str(round))
            for match in matches:
                match = bs4.BeautifulSoup(match, "html.parser")
                if match.find('th') != None and "Runde" in match.find('th').text: #it is not a match but a header for the round
                    continue
                #if it is the last row in the table, and thus not a match
                th = match.find('th')
                if th is not None and th.text.strip() == '':
                    continue
                currentMatch = self.rawSuperligaMatchToMatchObject(match)
                if currentMatch.date <= latestMatch.date: #if we have already looked at this match earlier
                    continue
                #if it has no score, it is in progress or havent been played (and from there on the rest of the matches are the same (except if they have been postponed))
                elif currentMatch.homeGoals == None or currentMatch.homeGoals == "": 
                    #Although we do not know if it is a postponed match yet, 
                    # we know that it should break in all circumstances if we are not skipping postponed matches
                    if not const.SKIP_POSTPONED_MATCHES: 
                        break
                    # if self.matchIsPostponed(rawMatch): #not sure how this looks on new superliga website
                        # continue
                    else:
                        break
                elif currentMatch.date == date.today(): #if it is today, we don't check it 
                    continue
                allMatches.append(currentMatch)
        return allMatches
                
    def rawSuperligaMatchToMatchObject(self,rawMatchData):      
        match = Match()
        #get all tds in this object
        matchDetails = rawMatchData.find_all('td')
        for i, detail in enumerate(matchDetails):
            #ignore first elem as we compare backwards, and seconds cause that is the weekday
            if i == 0 or i == 1: 
                continue
            current = detail.text
            prev = matchDetails[i-1].text
            updated = prev.replace(current,"").strip()
            #date
            if i == 2:
                match.date = util.dateAndTimeToDate(updated)
            #teams
            if i == 3:
                match.homeTeam,match.awayTeam = updated.split("-")
            #score
            if i == 4:
                #if the match has not been played yet
                if updated.strip() == "" or updated.strip() == "Optakt":
                    return match
                match.homeGoals,match.awayGoals = util.splitAndConvertToInt(updated,"-")
        return match
        
    
    #Turns the data of a raw match into a match object, and returns it
    def rawMatchToMatchObject(self,rawMatchData):
        match = Match()
        for info in rawMatchData:
            if info.get('data-stat') == "date":
                match.date = util.textToDate(info.text)
            elif info.get('data-stat') == "home_team":
                match.homeTeam = info.text
            elif info.get('data-stat') == "away_team":
                match.awayTeam = info.text
            elif info.get('data-stat') == "score":
                #if text is empty the match hasnt been played, and we return a match object with no score which will be handled later
                if info.text == None or info.text == "":
                    return match
                match.homeGoals,match.awayGoals = util.splitAndConvertToInt(info.text,"–")#for some reason this is not a dash (-), but instead – (which is not a dash)
        return match
    
    def matchIsPostponed(self,rawMatchData):
        for info in rawMatchData:
            if info.get('data-stat') == "notes":
                if info.text == "Match Postponed":
                    return True
        return False
        