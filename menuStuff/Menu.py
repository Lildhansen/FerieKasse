from locale import currency
import keyboard
import time
import json
import orjson
import os
import colorama
from classes.Player import Player

from classes.League import League

import utilities.constants as const
from .MenuItem import MenuItem


class Menu:
    def __init__(self,players,title):
        self.players = players;
        self.playerAndAvailableLeagues = {i : [] for i in players}
        self.currentPlayer = players[0]
        self.playerCount = len(players)
        self.title = title
        self.__selectedIndex = 0
        self.running = False
        self.round = 1
        self.endOfRound = False
        self.options = []
    def getSelectedIndex(self):
        return self.__selectedIndex
    def setupMenu(self):
        with open("./logs/teams.json","r",encoding='utf-8') as file:
            leagueDict = json.load(file)
        for leagueItem in leagueDict.keys():
            optionTitle = self.getOptionTitle(leagueItem)
            for player in self.playerAndAvailableLeagues.keys():
                self.playerAndAvailableLeagues[player].append(optionTitle)
            subMenu = SubMenu(self.players,optionTitle,self)
            subMenu.options = leagueDict[leagueItem]
            self.options.append(subMenu)
    def run(self):
        self.running = True
        os.system("cls")
        while self.running:
            self.displayMenu()
            self.readInput()
    def displayMenu(self):
        os.system("cls")
        print(self.title," - ",self.currentPlayer.name)
        self.printOptions()
    def getOptionTitle(self,league):
        leagueList = league.split(",")
        return leagueList[0] + "(" + leagueList[1] +")"
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
        self.running = False
        option = self.options[self.__selectedIndex]
        option.currentPlayer = self.currentPlayer
        os.system("cls")
        option.run()
    def printOptions(self):
        for i in range(len(self.options)):
            if (i == self.__selectedIndex):
                print("  >",end="")
            print(self.options[i].title)
    def nextPlayer(self):
        ##this function does not work properly
        if len(self.players[0].teams) == len(self.players[-1].teams):
            self.round += 1
        offset = 0
        if self.endOfRound:
            self.endOfRound = False
            return
        print(self.round)
        if self.round % 2 == 0: #even - then go backwards
            offset = -1
        else: #odd - then go forward
            offset = 1
        nextPlayerIndex = self.players.index(self.currentPlayer) + offset
        #print(nextPlayerIndex)
        #time.sleep(2)
        if nextPlayerIndex == self.playerCount: #if we are about to be out of bounds
            self.endOfRound = True
        self.currentPlayer = self.players[nextPlayerIndex]
        ##afhænger af:
        # om det er lige eller ulige runde
        # om vi først lige er nået enden, og derfor skal køre samme player igen, eller omvendt skal køre videre
        # 0 - 1 - 1 - 0 - 0 - 1 - 1 ...




class SubMenu(Menu):
    def __init__(self, players, title, menu):
        self.players = players;
        self.playerCount = len(players)
        self.title = title
        self.__selectedIndex = 0
        self.running = False
        self.options = []
        self.pickedOptions = []
        self.menu = menu
        self.currentPlayer = None
    def run(self):
        self.running = True
        while self.running:
            self.displayMenu()
            self.readInput()
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
                return
            elif (key == "esc"):
                self.running = False
                self.menu.running = True
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
        option = self.options.pop(self.__selectedIndex)
        self.pickedOptions.append(option)
        self.selectTeam(option)
        self.menu.nextPlayer()
    def selectTeam(self,option):
        self.currentPlayer.teams.append(option)
        self.running = False
        self.menu.running = True
    