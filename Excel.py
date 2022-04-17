#own modules
from classes.Player import Player
import utilities.util as util

#imports
import openpyxl
import os
#import xlsxwriter

class Excel:
    def __init__(self,leagues):
        self.leagues = leagues
        self.player = util.getPlayerObjectsFromFile() ##denne skal bruges i stedet for den under - og metoden til den under skal også fjernes
        self.playersTeamsDict = {}
        self.__getPlayersTeams()
    def __getPlayersTeams(self):
        file = open(r"./logs/leaguesAndTeams.txt","r",encoding="utf-8")
        for line in file.readlines():
            if ":" in line:
                continue
            else:
                splitLine = (util.removeInvalidLetters(line)).split(",")
                if not (splitLine[1] in self.playersTeamsDict):
                    self.playersTeamsDict[splitLine[1]] = []
                self.playersTeamsDict[splitLine[1]].append(splitLine[0])
        for player,teams in self.playersTeamsDict.items():
            print(player,teams)
    def deleteExcelFile(self):
        if (os.path.isfile("Feriekasse.xlsx")):
            os.remove("Feriekasse.xlsx")
    def setupExcelFile(self):
        wb = openpyxl.Workbook() # new workbook
        ws = wb.active #new worksheet
        ws.title = "Feriekasse"
        row = 1
        column = 1
        for player,teams in self.playersTeamsDict.items(): #todo - fix skrivning til excel (håber __getPlayersTeams works as intended)
            #first column set
            ws.cell(row,column,player)
            for team in teams:
                row += 1
                ws.cell(row,column,team) #when testing internally this should be just team (not team.name) instead
            row += 1
            ws.cell(row,column,"Total:")
            #second column set
            row = 1
            column += 1
            ws.cell(row,column,"Point:")
            for team in teams:
                row += 1
                ws.cell(row,column,0)
            row += 1
            ws.cell(row,column,f"=SUM({util.numberToExcelColumn(column)}{row-len(teams)}:{util.numberToExcelColumn(column)}{row-1})")
            row = 1
            column += 1

        #...
        wb.save("Feriekasse.xlsx")
        wb.close()

#myExcel = Excel()
#myExcel.deleteExcelFile()
#myExcel.setupExcelFile()