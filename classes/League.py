#libraries - standard or pip
import datetime
import json
from classes.myJsonEncoder import MyJsonEncoder as Encoder

#own libraries
from classes.Match import Match
from utilities.Webdriver import Webdriver as wd
import utilities.constants as const

class League:
    def __init__(self,name,country):
        self.name = name
        self.country = country.lower()
        self.driver = None
        self.teams = []
        self.matches = []
        self.searchText = f"{self.country} {self.name} results"
        self.newLatestMatch = None
    #will update "matches" with all matches after the date 
    #(and perhaps after a certain match - the last one taken)
    def getMatchesAfterLatestMatch(self,match=Match()):
        if match.date == None:
            if datetime.datetime.now().month > 7: #if we are in the first half of the season we must get all matches from this year till now
                match.date = datetime.date(datetime.datetime.now().year,7,15)
            else: #if we are in the final half of the season, we must get all matches from last year's season start till now
                match.date = datetime.date(datetime.datetime.now().year-1,7,15)
        self.driver = wd()
        self.driver.findLeagueUrl(self.searchText)
        self.matches = self.driver.getMatchesAfterLatestMatch(match,self) 
        self.driver.quit()
        self.saveLatestMatchCovered()
        self.filterMatches()
        
    def saveLatestMatchCovered(self):
        latestMatchJSON = json.dumps(self.newLatestMatch,cls=Encoder)
        
        #reading
        file = open(r"./logs/latestMatchCovered.json","r")
        leaguesAndCountries = json.load(file)
        file.close()
        
        leaguesAndCountries[f"{self.country},{self.name}"] = latestMatchJSON  
        
        #writing  
        file = open(r"./logs/latestMatchCovered.json","w")
        json.dump(leaguesAndCountries,file)
        file.close()
        
    #removes the matches that does not involve any of the teams (that is players' teams) in that league,
    def filterMatches(self):
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
                continue #needs to go all the way through the list - if both teams are player teams
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
            ##-----MANGLER IMPLEMENTATION FOR KUN DOBBELT VED HJEMMEKAMPE I SLUTSPILLET AF SUPERLIGA----
            match.points *= 0 if homeTeam.playerName == awayTeam.playerName else const.INDBYRDES_MULTIPLIER
    def findTeamByTeamName(self,teamName):
        for team in self.teams:
            if team.name.lower() == teamName.lower():
                return team
        raise Exception("team not found")
           