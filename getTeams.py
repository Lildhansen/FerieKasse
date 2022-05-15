import bs4
import orjson

from utilities.Webdriver import Webdriver as wd
import time

leaguesAndTeams = {"premier-league,England":[],"Bundesliga,Tyskland":[],"laliga,Spanien":[],"serie-a,Italien":[],"Superliga,Danmark":[]}

wd = wd()

#get teams and save them in leagueAndTeams dict
def getTeams():
    for league in leaguesAndTeams.keys():
        wd.findLeagueUrl(f"{league} results",True)
        time.sleep(1.3) #waiting for page to load
        html = wd.driver.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        teamRows = soup.find_all("tr", {"class": "imso-loa imso-hov"})
        for teamRow in teamRows:
            teamName = teamRow.find("span",{"class" : "ellipsisize hsKSJe"}).text
            if (teamName in leaguesAndTeams[league]):
                break
            leaguesAndTeams[league].append(teamName)
    wd.quit()
    print(len(leaguesAndTeams["Superliga"]))


def addTeamsToJsonFile():
    with open("./logs/teams.json","wb") as file:
        file.write(orjson.dumps(leaguesAndTeams))

if __name__ == "__main__":
    getTeams()
    addTeamsToJsonFile()