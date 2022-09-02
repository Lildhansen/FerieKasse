import os
import utilities.constants as const
import shutil

import helperMain
    
def removeFeriekasse(feriekasseDir):
    shutil.rmtree(feriekasseDir)
    feriekasseName = feriekasseDir.split("/")[-1]
    print(f"Feriekasse, {feriekasseName}, has been removed")
    
def handleRemoveFeriekasse():
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
            for subdir, dirs, files in os.walk("./data"):
                for dir in dirs:
                    removeFeriekasse(fr"./data/{dir}")
            print("All feriekasser has been removed")
        quit()
    if userInput == "n":
        print("cancelled")
        quit()
    
    if "," in userInput:
        feriekasser = helperMain.handleMultipleArgumentsForFeriekasser(userInput)
        for feriekasse in feriekasser:
            removeFeriekasse(fr"./data/{feriekasse}")
        print("The selected feriekasser has been removed")
        quit()
        
    const.FERIEKASSE_NAME = userInput
    feriekasseDir = fr"./data/{const.FERIEKASSE_NAME}"
    if not os.path.exists(feriekasseDir):
        print("This feriekasse does not exist")
        quit()
    prompt = ""
    while (prompt != "y" and prompt != "n"):
        prompt = input("are you sure you want to reset this feriekasse? (y/n) ")
    if (prompt == "y"):
        removeFeriekasse(feriekasseDir)   

if __name__ == "__main__":
    handleRemoveFeriekasse()