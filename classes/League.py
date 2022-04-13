#libraries - standard or pip
import datetime

#own libraries
from classes.Match import Match
from utilities.Webdriver import Webdriver as wd

class League:
    def __init__(self,name,country):
        self.name = name
        self.country = country.lower()
        self.driver = None
        self.teams = []
        self.matches = []
        self.searchText = f"{self.country} {self.name} results"
    def addToLeaguesTeamsAndLinksFile(self):
        file = open(r"./logs/leaguesTeamsAndLinks.txt","a+")
        file.write(f"{self.name},{self.searchText}:\n")
        for team in self.teams:
            file.write(f"{team.name},{team.player}\n")
        file.close()
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
            if not (match.homeTeam in self.teams or match.awayTeam in self.teams):
                self.matches.remove(match)
                continue
            elif (match.homeTeam in self.teams):
                match.homeTeamIsPlayerTeam = True
            if (match.awayTeam in self.teams):
                match.awayTeamIsPlayerTeam = True
    #calculates the points for all matches and saves the points in the match objects
    def calculatePointsForMatches(self):
        for match in self.matches:
            match.calculatePoints(self)