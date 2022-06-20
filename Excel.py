#own modules
from ast import Raise
import utilities.util as util

#imports
import openpyxl
import os
#import xlsxwriter

class Excel:
    def __init__(self,leagues=[]):
        self.leagues = leagues
        self.players = util.getPlayerObjectsFromFile()
        self.playersTeamsDict = {}
    
    #sets up the excel file. This is done when starting a game
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
                ws.cell(row,column,team)
            row += 1
            ws.cell(row,column,"Total:")
            #second column set
            row = 1
            column += 1
            ws.cell(row,column,"Point:")
            for team in player.teams:
                row += 1
                pointLocation = util.numberToExcelColumn(column) + str(row)
                ws[pointLocation] = "=0"
            row += 1
            ws.cell(row,column,f"=SUM({util.numberToExcelColumn(column)}{row-len(player.teams)}:{util.numberToExcelColumn(column)}{row-1})")
            row = 1
            column += 1
        wb.save("Feriekasse.xlsx")
        wb.close()
    #updates the excel file. this is done when a game is in progress
    def updateExcelFile(self,players):
        wb = openpyxl.load_workbook('Feriekasse.xlsx')
        ws = wb.active #new worksheet
        column = 1
        for player in players:
            for match in player.matches:
                self.updateTeamPointsInColumn(match,ws,column)
            column += 2
        wb.save("Feriekasse.xlsx")
        wb.close()
    #deletes the excel file. this is done when a game is over
    def deleteExcelFile(self):
        if (os.path.isfile("Feriekasse.xlsx")):
            os.remove("Feriekasse.xlsx")
    #updates the points in the excel file for a single match
    def updateTeamPointsInColumn(self,match,ws,column):
        row = 2
        while True:
            cell = ws.cell(row,column)
            if cell.value == "Total:":
                Raise(Exception("team not found in excel file"))
            if cell.value == match.homeTeam or cell.value == match.awayTeam:
                pointCell = ws.cell(row,column+1)
                pointCell.value += "+" + str(match.points)
                break
            row += 1
            
              
#myExcel = Excel()
#myExcel.updateExcelFile([])


#det bliver ikke rigtig regnet ud - fx chelsea man u 1-1 regnes vist til 5 i stedet for 10