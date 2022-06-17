import os
    
def resetFeriekasse():
    prompt = ""
    while (prompt != "y" and prompt != "n"):
        prompt = input("are you sure you want to reset the feriekasse? (y/n) ")
    if (prompt == "y"):
        os.remove("Feriekasse.xlsx")
        os.remove("latestMatchCovered.json")
        os.remove("leaguesAndTeams.json")
        print("... files removed")
    input("press enter to continue ...")

if __name__ == "__main__":
    resetFeriekasse()