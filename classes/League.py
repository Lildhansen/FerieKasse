#libraries - standard or pip
import codecs
import datetime
from datetime import date
import json
import orjson
from classes.myJsonEncoder import MyJsonEncoder as Encoder
import copy

#own libraries
from classes.Match import Match
from utilities.Soup import Soup
import utilities.constants as const

class League:
    def __init__(self,name,country):
        self.name = name
        self.country = country.lower()
        self.soup = None
        self.teams = []
        self.matches = []
        self.link = None
    #will update "matches" with all matches after the date 
    #(and perhaps after a certain match - the last one taken)
    def getMatchesAfterLatestMatch(self,match=Match()):
        if match.date == None:
            if datetime.datetime.now().month > 7: #if we are in the first half of the season we must get all matches from this year till now
                match.date = datetime.date(datetime.datetime.now().year,7,15)
            else: #if we are in the final half of the season, we must get all matches from last year's season start till now
                match.date = datetime.date(datetime.datetime.now().year-1,7,15)
        self.soup = Soup()
        self.soup.getLinkContent(self.link)
        self.matches = self.soup.getMatchesAfterLatestMatch(match) 
        self.saveLatestMatchCovered()
        self.filterMatches()

        
    def saveLatestMatchCovered(self):
        if len(self.matches) == 0:
            return
        latestMatch = copy.deepcopy(self.matches[-1])
        latestMatch.date = latestMatch.date.isoformat()
        latestMatchJSON = json.dumps(latestMatch,cls=Encoder)
        #reading
        with codecs.open(fr"./data/{const.FERIEKASSE_NAME}/latestMatchCovered.json","r") as file:
            leaguesAndCountries = json.load(file)
        
        leaguesAndCountries[f"{self.name},{self.country}"] = latestMatchJSON  
        
        #writing  
        with codecs.open(fr"./data/{const.FERIEKASSE_NAME}/latestMatchCovered.json","w") as file:
            json.dump(leaguesAndCountries,file)
        
    #removes the matches that does not involve any of the teams (that is players' teams) in that league,
    def filterMatches(self):
        ####this function does not work at the moment
        originalMatchList = self.matches.copy() #creates a copy of the list as to no alter the list mid-loop
        for match in originalMatchList:                  
            TeamInMatch = False            
            for team in self.teams:
                if (match.homeTeam == team.name):
                    match.homeTeamIsPlayerTeam = True
                    TeamInMatch = True
                if (match.awayTeam == team.name):
                    match.awayTeamIsPlayerTeam = True
                    TeamInMatch = True
                continue #needs to go all the way through the list (even if one team is player team) - to make sure we check for if both teams are player teams
            if not TeamInMatch:
                self.matches.remove(match)
    #remove matches, where the losing team is not one of the players' teams
    def removeMatchesYielding0Points(self):
        originalMatchList = self.matches.copy() #creates a copy of the list as to no alter the list mid-loop
        for match in originalMatchList:
            if (not match.draw):
                if (match.homeTeamIsWinner and not match.awayTeamIsPlayerTeam) or (not match.homeTeamIsWinner and not match.homeTeamIsPlayerTeam):
                    self.matches.remove(match)           
    #calculates the points for all matches and saves the points in the match objects
    def calculatePointsForMatches(self):
        for match in self.matches:
            match.calculatePoints()
            self.applyMatchMultipliers(match)
    #apply possible multipliers for the match - if it was an "indbyrdes" match
    def applyMatchMultipliers(self,match):
        if (match.homeTeamIsPlayerTeam and match.awayTeamIsPlayerTeam): #if it is an indbyrdes match
            homeTeam = self.findTeamByTeamName(match.homeTeam)
            awayTeam = self.findTeamByTeamName(match.awayTeam)
            if homeTeam.playerName == awayTeam.playerName:
                match.points *= 0
            elif self.isSlutspilMatch(match) and match.homeTeamIsWinner:
                return
            else:
                match.points *= const.INDBYRDES_MULTIPLIER
    def isSlutspilMatch(self,match):
        if self.name.lower() != "superliga":
            return False
        if match.date >= datetime.date(datetime.datetime.now().year,4,1):
            return True
            
    def findTeamByTeamName(self,teamName):
        for team in self.teams:
            if team.name.lower() == teamName.lower():
                return team
        raise Exception("team not found")
           