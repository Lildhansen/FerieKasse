#libraries - standard or pip

#own modules
from classes.Player import Player
import utilities.util as util
from utilities.Webdriver import Webdriver as wd
import helperMain


 
def UpdateFerieKasse():
    leagues = helperMain.getAllLeagues()
    #file = open("./logs/WeeksCovered.txt","r")
    for league in leagues:
        ##kunne godt bruge threads her
        league.getMatchesAfterLatestMatch()
        league.calculatePointsForMatches()
        return


if __name__ == "__main__":
    UpdateFerieKasse()

