import os
import datetime


class League:
    def __init__(self,name,country):
        self.name = name
        self.country = country.lower()
        self.driver = None
        self.teams = []
        self.matches = []
        self.url = self.getUrl()
    def getUrl(self):
        return f"https://www.flashscore.dk/fodbold/{self.country}/{self.name}/resultater/"
    def addToLeaguesTeamsAndLinksFile(self):
        file = open(r"./logs/leaguesTeamsAndLinks.txt","a+")
        file.write(f"{self.name},{self.url}:\n")
        for team in self.teams:
            file.write(f"{team.name},{team.player}\n")
        file.close()
    #will update "matches" with all matches after the date 
    #(and perhaps after a certain match - the last one taken)
    def getMatchesAfterDateAndMatch(self,date=datetime.date(datetime.now().year,7,15),hometeam=None,awayTeam=None):  
        anyMatchesLeft = True
        while anyMatchesLeft:
            anyMatchesLeft = False
