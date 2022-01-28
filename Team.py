import selenium
import bs4, requests
import constants as const
class Team:
    def __init__(self,name,league,country,player):
        self.name = name
        self.league = league
        self.country = country
        self.player = player
    def getMatchForTeam(self):
        res = self.establishConnection()
        soup = bs4.BeautifulSoup(res.text,"html.parser")
        elem = soup.find_all("div",class_="ui-table__header")
        print(elem)
    def establishConnection(self):
        res = requests.get(f"{const.LINK}/fodbold/{self.country}/{self.league}/tabeloversigt")
        res.raise_for_status()
        return res
        


