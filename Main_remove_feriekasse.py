import os
import utilities.constants as const
    
def resetFeriekasse():
    prompt = ""
    while (prompt != "y" and prompt != "n"):
        prompt = input("are you sure you want to reset the feriekasse? (y/n) ")
    if (prompt == "y"):
        if os.path.exists(fr"./data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx"):
            os.remove(fr"./data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx")
        if os.path.exists(fr"./data/{const.FERIEKASSE_NAME}/leaguesAndTeams.json"):
            os.remove(fr"./data/{const.FERIEKASSE_NAME}/leaguesAndTeams.json")
        if os.path.exists(fr"./data/{const.FERIEKASSE_NAME}/latestMatchCovered.json"):
            os.remove(fr"./data/{const.FERIEKASSE_NAME}/latestMatchCovered.json") 
        print("... files removed")
    input("press enter to continue ...")

if __name__ == "__main__":
    resetFeriekasse()