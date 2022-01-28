import bs4, requests
import constants as const
class Team:
    def __init__(self,name,league,player):
        self.name = name
        self.league = league
        self.player = player
    def getMatchForTeam(self):
        self.establishConnection()
    def establishConnection(self):
        res = requests.get(const.LINK)
        print(res.raise_for_status())


