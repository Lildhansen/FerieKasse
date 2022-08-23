import os
import utilities.constants as const
import shutil

import helperMain
    
def resetFeriekasse():
    print("removing a feriekasse")
    userInput = ""
    while userInput == ""  or userInput.lower() == "-l":
        userInput = input("What feriekasse would you like to remove? (n = cancel) (-a = remove all feriekasser) (-l = list all feriekasser) ")
        if userInput.lower() == "-l":
            helperMain.listAllFeriekasser()
    if userInput == "-a":
        prompt = ""
        while (prompt != "y" and prompt != "n"):
            prompt = input("are you sure you want to reset all feriekasser? (y/n) ")
        if (prompt == "y"):
            dataDir = fr"./data"
            for subdir, dirs, files in os.walk(dataDir):
                for dir in dirs:
                    shutil.rmtree(fr"{dataDir}/{dir}")
            print("All feriekasser has been removed")
        quit()
    if userInput == "n":
        print("cancelled")
        exit()
        
    const.FERIEKASSE_NAME = userInput
    feriekasseDir = fr"./data/{const.FERIEKASSE_NAME}"
    if not os.path.exists(feriekasseDir):
        print("This feriekasse does not exist")
        exit()
    prompt = ""
    while (prompt != "y" and prompt != "n"):
        prompt = input("are you sure you want to reset this feriekasse? (y/n) ")
    if (prompt == "y"):
        shutil.rmtree(feriekasseDir)
        print("Feriekasse removed")

if __name__ == "__main__":
    resetFeriekasse()