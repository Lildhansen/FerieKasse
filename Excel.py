#own modules
import utilities.util as util
import utilities.constants as const
import random

#imports
from ast import Raise
import openpyxl
import os
from openpyxl.styles import colors
from openpyxl.styles import Font, Color
#import xlsxwriter

class Excel:
    def __init__(self,leagues=[]):
        self.leagues = leagues
        self.players = util.getPlayerObjectsFromFile()
        self.playersTeamsDict = {}
        self.leaguesAndColors = {}
        self.addColorsToLeagues(self.leagues)
    
    #sets up the excel file. This is done when starting a game
    def addColorsToLeagues(self,leagues):
        availableColors = const.AVAILABLE_COLORS.copy()
        random.shuffle(const.AVAILABLE_COLORS)
        for league in leagues:
            self.leaguesAndColors[league.name] = availableColors[0]
            availableColors.pop(0)
            
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
                ws.cell(row,column,team.name)
                ws[f"{util.numberToExcelColumn(column)}{row}"].font = Font(color=Color(self.leaguesAndColors[team.leagueName]))
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
            ws.cell(row,column,f"=SUM({util.numberToExcelColumn(column)}{row - len(player.teams)}:{util.numberToExcelColumn(column)}{row-1})")
            row = 1
            column += 1
        for league in self.leagues:
            row += 1
            ws.cell(row,column,league.name)
            ws[f"{util.numberToExcelColumn(column)}{row}"].font = Font(color=Color(self.leaguesAndColors[league.name]))
        wb.save(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx")
        wb.close()
    #updates the excel file. this is done when a game is in progress
    def updateExcelFile(self,players):
        wb = openpyxl.load_workbook(fr'data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx')
        ws = wb.active #new worksheet
        column = 1
        for player in players:
            for match in player.matches:
                self.updateTeamPointsInColumn(match,ws,column)
            column += 2
        if const.FOUR_GOAL_WIN_RULE:
            self.addFourGoalWinBonusPoints(ws,players)
        wb.save(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx")
        wb.close()
    #adds bonus points for for four goal win rule
    def addFourGoalWinBonusPoints(self,ws,players):
        column = 1
        row = 1
        for player in players:
            while True:
                if player.name == ws.cell(row,column).value:
                    break
                column += 2
            for team in player.teams:
                row = 1
                if team.bonusPoints == 0:
                    continue
                cell = ws.cell(row,column)
                if team.name == cell.value:
                    pointCell = ws.cell(row,column+1)
                    pointCell.value += "+" + str(team.bonusPoints)
                else:
                    row += 1
                
                
        
    #deletes the excel file. this is done when a game is over
    def deleteExcelFile(self):
        if (os.path.isfile(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx")):
            os.remove(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx")
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