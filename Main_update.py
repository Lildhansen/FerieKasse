#libraries - standard or pip

#own modules
from classes.Team import Team
from classes.Player import Player
import utilities.util as util
from utilities.Webdriver import Webdriver as wd
import helperMain

driver = wd()

 
def UpdateFerieKasse():
    leagues = helperMain.getAllLeagues()
    #file = open("./logs/WeeksCovered.txt","r")
    for league in leagues:
        print(league.name)
        league.driver = driver
        league.getMatchesAfterDateAndMatch()
        driver.quit()
        return


if __name__ == "__main__":
    UpdateFerieKasse()

