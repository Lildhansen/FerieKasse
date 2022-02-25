class Player:
    def __init__(self,name,teams):
        self.name = name
        self.teams = teams 
        self.menu = None
    #how teams are to be added - by appending to the list
    def addTeam(self,team):
        self.teams.append(team)
    #adds players and teams to the .txt-file with players, teams and URLs
    def addToPlayersTeamsAndLinksFile(self):
        file = open(r"./logs/playersTeamsAndLinks.txt","a+")
        file.write(f"{self.name}:\n")
        for team in self.teams:
            file.write(f"{team.name},{team.url}\n")
        file.close()

