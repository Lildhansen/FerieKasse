import os
    
def resetFeriekasse():
    prompt = ""
    while (prompt != "y" and prompt != "n"):
        prompt = input("are you sure you want to reset the feriekasse? (y/n) ")
    if (prompt == "y"):
        if os.path.exists("Feriekasse.xlsx"):
            os.remove("Feriekasse.xlsx")
        if os.path.exists("./logs/leaguesAndTeams.json"):
            os.remove("./logs/leaguesAndTeams.json")
        if os.path.exists("./logs/latestMatchCovered.json"):
            os.remove("./logs/latestMatchCovered.json") 
        print("... files removed")
    input("press enter to continue ...")

if __name__ == "__main__":
    resetFeriekasse()