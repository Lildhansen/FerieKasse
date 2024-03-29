import orjson

from utilities.Soup import Soup

leaguesAndTeams = {"premier-league,england":[],"bundesliga,tyskland":[],"laliga,spanien":[],"serie-a,italien":[],"superliga,danmark":[]}
def getLinks(league):
    if league == "superliga,danmark":
        return "https://fbref.com/en/comps/50/Superliga-Stats"
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