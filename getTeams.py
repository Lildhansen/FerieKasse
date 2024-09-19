import datetime
import orjson
from datetime import datetime

from utilities.Soup import Soup

leaguesAndTeams = {"premier-league,england":[],"bundesliga,tyskland":[],"laliga,spanien":[],"serie-a,italien":[],"superliga,danmark":[]}
def getLinks(league):
    if league == "superliga,danmark":
            if datetime.now().month > 7:
                return f"https://superstats.dk/program?aar={datetime.now().year}%2F{datetime.now().year+1}"
            else:
                return f"https://superstats.dk/program?aar={datetime.now().year-1}%2F{datetime.now().year}"
    elif league == "premier-league,england":
        return "https://fbref.com/en/comps/9/Premier-League-Stats"
    elif league == "bundesliga,tyskland":
        return "https://fbref.com/en/comps/20/Bundesliga-Stats"
    elif league == "serie-a,italien":
        return "https://fbref.com/en/comps/11/Serie-A-Stats"
    elif league == "laliga,spanien":
        return "https://fbref.com/en/comps/12/La-Liga-Stats"
soup = Soup()

#get teams and save them in leagueAndTeams dict
def getTeams():
    for league in leaguesAndTeams.keys():
        soup.getLinkContent(getLinks(league))
        if league == "superliga,danmark":
            table = soup.soup.find('table', {'id': 'tabel1'})
            for row in table.find('tbody').find_all('tr'):
                TeamName = row.find_all('td')[1]
                if TeamName.span:
                    TeamName.span.decompose()
                teamName = TeamName.text.strip()
                leaguesAndTeams[league].append(teamName)
            continue
        table = soup.soup.find("tbody")
        for team in table.find_all("tr"):
            for column in team.find_all("td"):
                if column.get("data-stat") == "team" and len(column.text) > 0: #this does not work
                    teamName = column.text.strip()
                    leaguesAndTeams[league].append(teamName)
#fjern tomme fra superliga (hul mellem mesterskabsspil og taberspil)

def addTeamsToJsonFile():
    with open("./data/teams.json","wb") as file:
        file.write(orjson.dumps(leaguesAndTeams))

if __name__ == "__main__":
    getTeams()
    addTeamsToJsonFile()