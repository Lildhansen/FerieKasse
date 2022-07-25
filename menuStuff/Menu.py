import keyboard
import time
import json
import json
import os
import colorama
import copy


import utilities.constants as const

#todo
"""
den er kinda ustabil
    den kører igen (kun 1 gang til) hvis den crasher
    hvis man trykker enter i lidt for lang tid registrerer den  det for begge
har ikke testet for mere end 2 spillere
clean up
comments
tests?
"""


        

class Menu:
    def __init__(self,players,title):
        self.players = players
        self.playerAndAvailableLeagues = {i : [] for i in players}
        self.currentPlayer = players[0]
        self.playerCount = len(players)
        self.title = title
        self.__selectedIndex = 0
        self.running = False
        self.round = 1
        self.endOfRound = False
        self.teamsPickedCount = 0
        self.lastRound = False
        time.sleep(4)
    def getSelectedIndex(self):
        return self.__selectedIndex
    def setupMenu(self):
        with open("./data/teams.json","r",encoding='utf-8') as file:
            leagueDict = json.load(file)
        for leagueItem in leagueDict.keys():
            optionTitle = self.getOptionTitle(leagueItem)
            subMenu = SubMenu(self.players,optionTitle,self)
            subMenu.options = leagueDict[leagueItem]
            for player in self.players:
                player.availableLeagues.append(subMenu)
    def setupLastRound(self):
        for player in self.players:
            for league in player.pickedLeagues:
                player.availableLeagues.append(league)
    def run(self):
        self.running = True
        os.system("cls")
        while self.running:
            #if final round
            if (self.currentPlayer.availableLeagues == []):
                self.lastRound = True
                self.setupLastRound()
            #if we are done
            if (self.round == const.TEAMS_PER_PLAYER+1):
                self.running = False
                return
            self.displayMenu()
            self.readInput()
    def displayMenu(self):
        os.system("cls")
        if (self.lastRound):
            print("-----Last round - every league is available now-----\n")
        print(self.title," - ",self.currentPlayer.name)
        self.printOptions()
    def getOptionTitle(self,league):
        leagueList = league.split(",")
        return leagueList[0] + "(" + leagueList[1] +")"
        #does the reverse of getOptionTitle - returns a string of the form "team,player"
    def unGetOptionTitle(self,league):
        return league.replace("(",",").replace(")","")
         
    def readInput(self):
        i = 0
        while True:
            time.sleep(.1)
            key = keyboard.read_key()
            if (key=="pil op"):
                self.moveUp()
                return
            elif (key =="pil ned"):
                self.moveDown()
                return
            elif (key == "enter"):
                self.selectOption()
                time.sleep(.1)
                return
            elif (key == "esc"):
                prompt = ""
                while (prompt != "y" and prompt != "n"):
                    prompt = input("are you sure you want to exit? (y/n) ")
                if (prompt == "y"):
                    self.running = False
                return
    def moveUp(self):
        time.sleep(.1)
        if (self.__selectedIndex - 1 < 0):
            self.__selectedIndex = len(self.currentPlayer.availableLeagues)-1
        else:
            self.__selectedIndex -= 1
    def moveDown(self):
        time.sleep(.1)
        if (self.__selectedIndex + 1 >= len(self.currentPlayer.availableLeagues)):
            self.__selectedIndex = 0
        else:
            self.__selectedIndex += 1
    def selectOption(self):
        time.sleep(.1)
        #self.running = False
        option = self.currentPlayer.availableLeagues[self.__selectedIndex]
        option.currentPlayer = self.currentPlayer
        os.system("cls")
        if option.run() == False:
            return
        self.teamsPickedCount += 1
        self.nextPlayer()
        self.__selectedIndex = 0 #sets picker pointer to top of menu (avoids index out of bounds error)
    def printOptions(self):
        #if last round
        if (self.lastRound == True):
            for i in range(len(self.currentPlayer.availableLeagues)):
                if (i == self.__selectedIndex):
                    print("  >",end="")
                print(self.currentPlayer.availableLeagues[i].title)
            return
        for i in range(len(self.currentPlayer.availableLeagues)):
            if (i == self.__selectedIndex):
                print("  >",end="")
            print(self.currentPlayer.availableLeagues[i].title,end=" - mangler at vælge denne liga: ")
            for player in self.players:
                for league in player.availableLeagues:
                    if league == self.currentPlayer.availableLeagues[i]:
                        print(player.name,end=",")
                        break
            print("")
        if (len(self.currentPlayer.pickedLeagues) == 0):
            return
        print("\nunavailable leagues: ")
        for league in self.currentPlayer.pickedLeagues:
            print(colorama.Fore.RED,league.title,colorama.Style.RESET_ALL)
    def nextPlayer(self):
        if (self.teamsPickedCount % self.playerCount == 0 and self.teamsPickedCount != 0): #if end of round
            self.round += 1
            return
        if self.round % 2 == 0: #if even - then go backwards (since we start at round 1)
            offset = -1
        else: #if odd - then go forward
            offset = 1
        nextPlayerIndex = self.players.index(self.currentPlayer) + offset
        print(nextPlayerIndex)
        self.currentPlayer = self.players[nextPlayerIndex]
        self.run()
    
    def saveInJson(self):
        jsonData = copy.deepcopy(const.LeagueNationsDict)
        #save jsonData and then overwrite it with the new data
        for player in self.players:
            for league in player.pickedLeagues:
                for team in player.teams:
                    for pickedTeam in league.pickedOptions:
                        if pickedTeam == team:
                            jsonData[self.unGetOptionTitle(league.title)].update({team:player.name})
        with open(fr"./data/{const.FERIEKASSE_NAME}/leaguesAndTeams.json","w") as file:
            file.write(json.dumps(jsonData))

class SubMenu(Menu):
    def __init__(self, players, title, menu):
        self.players = players
        self.playerCount = len(players)
        self.title = title
        self.__selectedIndex = 0
        self.running = False
        self.hasExitted = False
        self.menu = menu
        self.options = [] #list of strings
        self.pickedOptions = [] #list of strings
        self.currentPlayer = None
    def run(self):
        self.__selectedIndex = 0 #sets picker pointer to top of menu (avoids index out of bounds error)
        self.running = True
        self.hasExitted = False
        while self.running:
            self.displayMenu()
            self.readInput()
            if self.hasExitted:
                return False
    def displayMenu(self):
        os.system("cls")
        print(self.title," - ",self.currentPlayer.name)
        self.printOptions()
    def getOptionTitle(self,league):
        leagueList = league.split(",")
        return leagueList[0] + "(" + leagueList[1] +")"
    def printOptions(self):
        for i in range(len(self.options)):
            if (i == self.__selectedIndex):
                print("  >",end="")
            print(self.options[i])
        if (len(self.pickedOptions) != 0):
            print("\n picked teams: ")
        for option in self.pickedOptions:
            print(colorama.Fore.RED,option,colorama.Style.RESET_ALL)
    def readInput(self):
        i = 0
        while True:
            key = keyboard.read_key()
            if (key=="pil op"):
                self.moveUp()
                return
            elif (key =="pil ned"):
                self.moveDown()
                return
            elif (key == "enter"):
                self.selectOption()
                time.sleep(.1)
                return
            elif (key == "esc"):
                self.running = False
                self.hasExitted = True
                return
    def moveUp(self):
        time.sleep(.1)
        if (self.__selectedIndex - 1 < 0):
            self.__selectedIndex = len(self.options)-1
        else:
            self.__selectedIndex -= 1
    def moveDown(self):
        time.sleep(.1)
        if (self.__selectedIndex + 1 >= len(self.options)):
            self.__selectedIndex = 0
        else:
            self.__selectedIndex += 1
    def selectOption(self):
        time.sleep(.1)
        option = self.options.pop(self.__selectedIndex)
        self.pickedOptions.append(option)
        self.selectTeam(option)
    def selectTeam(self,option):
        time.sleep(.1)
        self.currentPlayer.teams.append(option)
        self.currentPlayer.availableLeagues.remove(self)
        #for player in self.players:
        #    player.pickedLeagues.append(self)
        self.currentPlayer.pickedLeagues.append(self)
        self.running = False
        
    