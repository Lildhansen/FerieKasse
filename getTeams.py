import orjson
import requests


leaguesAndTeams = {"eng.1":[],"ger.1":[],"esp.1":[],"ita.1":[],"den.1":[]}

#get teams and save them in leagueAndTeams dict
def getTeams():
    for league in leaguesAndTeams.keys():
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/teams"
        resp = requests.get(url)
        data = resp.json()
        for team in data.get("sports", [])[0].get("leagues", [])[0].get("teams", []):
            teamName = team.get("team", {}).get("displayName", "Unknown Team")
            leaguesAndTeams[league].append(teamName)
            
def addTeamsToJsonFile():
    with open("./data/teams.json","wb") as file:
        file.write(orjson.dumps(leaguesAndTeams))

if __name__ == "__main__":
    getTeams()
    addTeamsToJsonFile()