import pytest
from Excel import Excel
from classes.League import League
import utilities.constants as const
import os
import openpyxl

def setupMockExcelFile():
    const.FERIEKASSE_NAME = "unitTests/excelTest"
    if os.path.exists(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx"):
        os.remove(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx")
    league1 = League("league1","country1")
    league2 = League("league2","country2")
    league3 = League("league3","country3")
    return Excel([league1,league2,league3])

def test_excel_init_adds_colors_to_leagues():
    excel = setupMockExcelFile()
    assert excel.leaguesAndColors["league1"] != None
    assert excel.leaguesAndColors["league2"] != None
    assert excel.leaguesAndColors["league3"] != None

def test_excel_file_can_be_deleted():
    excel = setupMockExcelFile()
    with open(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx", "w"):
        pass
    assert os.path.exists(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx")
    excel.deleteExcelFile()
    assert not os.path.exists(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx")
    
def test_setupExcelFile_creates_excel_file():
    excel = setupMockExcelFile()
    excel.deleteExcelFile()
    excel.setupExcelFile()
    assert os.path.exists(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx")

#this is a beautiful test
def test_setupExcelFile_formats_excel_file_correctly():
    excel = setupMockExcelFile()
    excel.deleteExcelFile()
    excel.setupExcelFile()
    
    #load newly created excel file
    wb = openpyxl.load_workbook(fr'data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx')
    ws = wb.active #current worksheet
    assert ws.cell(1,1).value == excel.players[0].name
    assert ws.cell(2,1).value == excel.players[0].teams[0].name
    assert ws.cell(3,1).value == excel.players[0].teams[1].name
    assert ws.cell(4,1).value == "Total:"
    
    assert ws.cell(1,2).value == "Point:"
    assert ws.cell(2,2).value == "=0"
    assert ws.cell(3,2).value == "=0"
    assert ws.cell(4,2).value == "=SUM(B2:B3)"
    
    assert ws.cell(1,3).value == excel.players[1].name
    assert ws.cell(2,3).value == excel.players[1].teams[0].name
    assert ws.cell(3,3).value == excel.players[1].teams[1].name
    assert ws.cell(4,3).value == "Total:"
    
    assert ws.cell(1,4).value == "Point:"
    assert ws.cell(2,4).value == "=0"
    assert ws.cell(3,4).value == "=0"
    assert ws.cell(4,4).value == "=SUM(D2:D3)"
    
    assert ws.cell(1,5).value == None
    assert ws.cell(2,5).value == excel.leagues[0].name
    assert ws.cell(3,5).value == excel.leagues[1].name
    assert ws.cell(4,5).value == excel.leagues[2].name
    


###integration tests:
#update excel file - setup excel file first - so integration test
#update team points in column - setup excel file first - so integration test
#getPlayerScoreFromExcelFile - setup excel file first - so integration test
#get team - only the 2 specific functions are tested (rather than the getTeam function) - setup excel file first - so integration test









#const.FERIEKASSE_NAME = "unitTests/extraBodyTrailingTrue"