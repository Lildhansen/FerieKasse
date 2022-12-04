#libraries - standard or pip
from datetime import date
import time
import bs4, requests

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
        time.sleep(2)
        with requests.Session() as req:
            self.res = req.get(link)
            while self.res.status_code == 429:
                #time.sleep(int(self.res.headers["Retry-After"]))
                time.sleep(.5)
                self.res = req.get(link)
            self.res.raise_for_status()
        self.soup = bs4.BeautifulSoup(self.res.text,features="lxml")
    #takes the latest match that has been processed as input, and get all matches in that specific league between that match+1 and the last played match
    def getMatchesAfterLatestMatch(self,latestMatch):
        allMatches = []
        for rawMatch in self.soup.findAll('tr'):
            if len(rawMatch.text) == 0 or rawMatch.text == None:
                continue
            elif not rawMatch.text[0].isdigit(): 
                continue
            #then it is indeed a match
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
        