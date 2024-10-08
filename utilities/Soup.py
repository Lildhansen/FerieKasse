#libraries - standard or pip
from datetime import date
import time
import bs4
import requests

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
        with requests.Session() as req:
            self.res = req.get(link)
            while self.res.status_code == 429:
                #time.sleep(int(self.res.headers["Retry-After"]))
                time.sleep(.5)
                self.res = req.get(link)
            self.res.raise_for_status()
        self.soup = bs4.BeautifulSoup(self.res.text,"html.parser")
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
        # print(f"({allRounds})")
        for round in allRounds:
            for match in round.find_all('tr'):
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
        # print(rawMatchData)
        #get all tds in this object
        matchDetails = rawMatchData.find_all('td')
        match.date = util.dateAndTimeToDate(matchDetails[1].text)
        match.homeTeam,match.awayTeam = matchDetails[2].text.split("-")
        score = matchDetails[3].text
        if score.strip() == "": #if the match has not been played yet
            return match
        match.homeGoals,match.awayGoals = util.splitAndConvertToInt(matchDetails[3].text,"-")
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
        