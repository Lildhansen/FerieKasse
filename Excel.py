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
        self.players = util.getPlayerObjectsFromFile() ##denne skal bruges i stedet for den under - og metoden til den under skal også fjernes
        self.playersTeamsDict = {}
    def deleteExcelFile(self):
        if (os.path.isfile("Feriekasse.xlsx")):
            os.remove("Feriekasse.xlsx")
    def setupExcelFile(self):
        wb = openpyxl.Workbook() # new workbook
        ws = wb.active #new worksheet
        ws.title = "Feriekasse"
        row = 1
        column = 1
        for player in self.players: #todo - fix skrivning til excel (håber __getPlayersTeams works as intended)
            #first column set
            ws.cell(row,column,player.name)
            for team in player.teams:
                row += 1
                ws.cell(row,column,team) #when testing internally this should be just team (not team.name) instead
            row += 1
            ws.cell(row,column,"Total:")
            #second column set
            row = 1
            column += 1
            ws.cell(row,column,"Point:")
            for team in player.teams:
                row += 1
                ws.cell(row,column,0)
            row += 1
            ws.cell(row,column,f"=SUM({util.numberToExcelColumn(column)}{row-len(player.teams)}:{util.numberToExcelColumn(column)}{row-1})")
            row = 1
            column += 1

        #...
        wb.save("Feriekasse.xlsx")
        wb.close()
    def updateExcelFile(self,players):
        pass
        #open file
        #for hver spiller (her skal kolonnerne skippe med 2)
            #for hver kamp
                #find det hold (hometeam == hold eller awayteam == hold) som matcher
                #indsæt point
#myExcel = Excel()
#myExcel.deleteExcelFile()
#myExcel.setupExcelFile()