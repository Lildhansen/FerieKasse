import os


class League:
    def __init__(self,name,country):
        self.name = name
        self.country = country.lower()
        self.teams = []
        self.url = self.getUrl()
    def getUrl(self):
        return f"https://www.flashscore.dk/fodbold/{self.country}/{self.name}/resultater/"
    def addToLeaguesTeamsAndLinksFile(self):
        file = open(r"./logs/leaguesTeamsAndLinks.txt","a+")
        file.write(f"{self.name},{self.url}:\n")
        for team in self.teams:
            file.write(f"{team.name},{team.player}\n")
        file.close()