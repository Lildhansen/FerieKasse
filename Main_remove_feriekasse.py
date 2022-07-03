import os
import utilities.constants as const
import shutil
    
def resetFeriekasse():
    print("removing a feriekasse")
    userInput = ""
    print(userInput != "")
    print(not userInput.isspace())
    while userInput == "" or userInput.isspace():
        userInput = input("What feriekasse would you like to remove? (n = cancel) (all = remove all feriekasser) ") #add remove all option
    if userInput == "all":
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