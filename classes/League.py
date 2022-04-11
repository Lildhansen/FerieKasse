import os
import datetime


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
    def getMatchesAfterDateAndMatch(self,date=datetime.date(datetime.datetime.now().year,7,15),hometeam=None,awayTeam=None):
        self.driver.findLeagueUrl(self.searchText)
        self.matches = self.driver.getMatchesAfterDateAndMatch(date,self.teams) 
