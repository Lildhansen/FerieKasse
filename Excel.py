#own modules
from classes.Player import Player
import utilities.util as util

#imports
import openpyxl
import os
#import xlsxwriter

class Excel:
    def __init__(self,players=None):
        self.players = players
        if players == None:
            self.players = []
            self.__getPlayers()
    def __getPlayers(self):#for testing purposes
        file = open(r"./logs/PlayerAndTeams.txt","r",encoding="utf-8")
        for line in file.readlines():
            if ":" in line.lower():
                self.players.append(Player((line.rstrip()).strip(":"),[]))
            else:
                strippedSplitLine = util.removeInvalidLetters(line.rstrip()).split(",")
                self.players[-1].addTeam(strippedSplitLine[0])
    def deleteExcelFile(self):
        if (os.path.isfile("Feriekasse.xlsx")):
            os.remove("Feriekasse.xlsx")
    def setupExcelFile(self):
        wb = openpyxl.Workbook() # new workbook
        ws = wb.active #new worksheet
        ws.title = "Feriekasse"
        row = 1
        column = 1
        for player in self.players:
            #first column set
            ws.cell(row,column,player.name)
            for team in player.teams:
                row += 1
                ws.cell(row,column,team.name) #when testing internally this should be just team (not team.name) instead
            row += 1
            ws.cell(row,column,"Total:")
            #second column set
            row = 1
            column += 1
            ws.cell(row,column,"Point")
            for team in player.teams:
                row += 1
                ws.cell(row,column,0)
            row += 1
            ws.cell(row,column,f"=SUM({util.numberToCharValue(column)}{row-len(player.teams)}:{util.numberToCharValue(column)}{row-1})")
            row = 1
            column += 1

        #...
        wb.save("Feriekasse.xlsx")
        wb.close()

#myExcel = Excel()
#myExcel.deleteExcelFile()
#myExcel.setupExcelFile()