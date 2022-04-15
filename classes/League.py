#libraries - standard or pip
import datetime

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
        self.matches = self.driver.getMatchesAfterLatestMatch(match)    
        self.driver.quit()
        self.filterMatches()
    #removes the matches that does not involve any of the teams (that is players' teams) in that league
    def filterMatches(self):
        for match in self.matches:
            if not (match.homeTeam in self.teams.name or match.awayTeam in self.teams.name):
                self.matches.remove(match)
                continue
            elif (match.homeTeam in self.teams.name):
                match.homeTeamIsPlayerTeam = True
            if (match.awayTeam in self.teams.name):
                match.awayTeamIsPlayerTeam = True
    #calculates the points for all matches and saves the points in the match objects
    def calculatePointsForMatches(self):
        for match in self.matches:
            match.calculatePoints(self)
            self.applyMatchMultipliers(match)
    #apply possible multipliers for the match - if it was an "indbyrdes" match
    def applyMatchMultipliers(self,match):
        if (match.awayTeamIsPlayerTeam and match.awayTeamIsPlayerTeam): #if it is an indbyrdes match
            homeTeam = self.findTeamByTeamName(match.homeTeam)
            awayTeam = self.findTeamByTeamName(match.awayTeam)
            ##-----MANGLER IMPLEMENTATION FOR KUN DOBBELT VED HJEMMEKAMPE I SLUTSPILLET AF SUPERLIGA----
            match.points *= 0 if homeTeam.playerName == awayTeam.playerName else const.INDBYRDES_MULTIPLIER
    def findTeamByTeamName(self,teamName):
        for team in self.teams:
            if team.name.lower() == teamName.lower():
                return team
        raise Exception("team not found")
           