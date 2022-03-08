#own modules
from classes.Player import Player
import utilities.util as util

#imports
import openpyxl
#import xlsxwriter

class Excel:
    def __init__(self,players=None):
        self.players = []
        if players == None:
            self.__getPlayers()
    def __getPlayers(self):#for testing purposes
        file = open(r"./logs/PlayerAndTeams.txt","r",encoding="utf-8")
        for line in file.readlines():
            if ":" in line.lower():
                self.players.append(Player((line.rstrip()).strip(":"),[]))
            else:
                strippedSplitLine = util.removeInvalidLetters(line.rstrip()).split(",")
                self.players[-1].addTeam(strippedSplitLine)
    def setupExcelFile(self):
        wb = openpyxl.Workbook() # new workbook
        ws = wb.active #new worksheet
        ws.title = "Feriekasse"
        
        #...
        wb.save("Feriekasse.xlsx")
        wb.close()

myExcel = Excel()
myExcel.setupExcelFile()