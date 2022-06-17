import bs4
import orjson

from utilities.Soup import Soup
import time

leaguesAndTeams = {"premier-league,england":[],"bundesliga,tyskland":[],"laliga,spanien":[],"serie-a,italien":[],"superliga,danmark":[]}

Soup = Soup()

#get teams and save them in leagueAndTeams dict
def getTeams():
    for league in leaguesAndTeams.keys():
        Soup.findLeagueUrl(f"{league} results",True)
        time.sleep(1.3) #waiting for page to load
        html = Soup.driver.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        teamRows = soup.find_all("tr", {"class": "imso-loa imso-hov"})
        for teamRow in teamRows:
            teamName = teamRow.find("span",{"class" : "ellipsisize hsKSJe"}).text
            if (teamName in leaguesAndTeams[league]):
                break
            leaguesAndTeams[league].append(teamName)
    Soup.quit()
    print(len(leaguesAndTeams["superliga"]))


def addTeamsToJsonFile():
    with open("./logs/teams.json","wb") as file:
        file.write(orjson.dumps(leaguesAndTeams))

if __name__ == "__main__":
    getTeams()
    addTeamsToJsonFile()