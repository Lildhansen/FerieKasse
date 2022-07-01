import os
import utilities.constants as const
import shutil
    
def resetFeriekasse():
    print("removing a feriekasse")
    const.FERIEKASSE_NAME = input("What feriekasse would you like to remove? (n to cancel) ")
    if const.FERIEKASSE_NAME == "n":
        print("cancelled")
        exit()
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