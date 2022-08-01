class Team():
    def __init__(self,name,playerName,leagueName=""):
        self.name = name
        self.playerName = playerName
        self.leagueName = leagueName
        self.bonusPoints = 0
        self.points = 0 #used for Email

