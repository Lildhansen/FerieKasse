from collections import namedtuple
import datetime
import pytest
from datetime import date
import utilities.util as util
from classes.Player import Player
from classes.Team import Team
import utilities.constants as const
from freezegun import freeze_time

import json

@pytest.mark.parametrize("test_input", [("data"),("Feriekasse..."),("123AbC")])
def test_folderIsValid_returns_True_for_valid_folder_names(test_input):
    assert util.folderIsValid(test_input) == True

@pytest.mark.parametrize("test_input", [("a/b/c"),("a,b,c"),("/ss\\a:*xz?sad\"54<12>1|,"),(""),("    "),("a -l")])
def test_folderIsValid_returns_False_for_invalid_folder_names(test_input):
    assert util.folderIsValid(test_input) == False

def test_parseIntOrNone_parses_int_correctly():
    assert util.parseIntOrNone("100")==100

@pytest.mark.parametrize("test_input", [("2.5"),("abcdef"),("")])
def test_parseIntOrNone_returns_None_if_input_cannnot_be_int(test_input):
    assert util.parseIntOrNone(test_input) == None
    
@pytest.mark.parametrize("test_input,expected", [("2.5",2.5),("10",10)])    
def test_parseFloatOrNone_parses_float_correctly(test_input,expected):
    assert util.parseFloatOrNone(test_input)==expected

@pytest.mark.parametrize("test_input", [("abcdef"),("")])
def test_parseFloatOrNone_returns_None_if_input_cannnot_be_float(test_input):
    assert util.parseFloatOrNone(test_input) == None
    
@pytest.mark.parametrize("test_input", [("1"),(1),("True")])
def test_parseBool_returns_true_if_passed_truthy_value(test_input):
    assert util.parseBool(test_input) == True

@pytest.mark.parametrize("test_input", [(123),("this is False"),(""),(None)])
def test_parseBool_returns_false_if_passed_non_truthy_values(test_input):
    assert util.parseBool(test_input) == False
        
@pytest.mark.parametrize("test_input,expected", [(1, "A"), (26,"Z"),(27,"AA"),(53, "BA"),(14,"N"),(79,"CA"),(26*27,"ZZ")]) 
#ZZ is max value. for 3 digits it omits one of the digits (fx AAA is AA instead) 
# though it doesnt matter cause that many players will never play it
def test_numberToExcelColumn_returns_correct_columnstring(test_input,expected):
    assert util.numberToExcelColumn(test_input) == expected

@pytest.mark.parametrize("test_input,expected", [("1+3+5+1",10),("=1",1)])      
def test_getSumOfExcelCell_returns_correct_sum(test_input,expected):
    assert util.getSumOfExcelCell(test_input) == expected

@pytest.mark.parametrize("test_input,expected", [("1,2,3,4,5",[1,2,3,4,5]),("1,2,None",[1,2,None])])  
def test_splitAndConvertToInt_returns_correct_list(test_input,expected):
    assert util.splitAndConvertToInt(test_input,",") == expected

def test_textToDate_converts_correctly():
    assert util.textToDate("2022-01-01") == date(2022,1,1)

@freeze_time("2022-09-09")
@pytest.mark.parametrize("test_input,expected", [("03/03 14.00",date(2022,3,3)),("10/10 14.00",date(2022,10,10))])
def test_dateAndTimeToDate_converts_correctly_if_we_are_in_first_half_of_season(test_input,expected):
    assert util.dateAndTimeToDate(test_input) == expected

@freeze_time("2023-03-03")
@pytest.mark.parametrize("test_input,expected", [("02/02 14.00",date(2023,2,2)),("10/10 14.00",date(2022,10,10))])
def test_dateAndTimeToDate_converts_correctly_if_we_are_in_second_half_of_season(test_input,expected):
    assert util.dateAndTimeToDate(test_input) == expected

@pytest.mark.parametrize("test_input,expected", [("FCM","Midtjylland"),("FCK","FC Copenhagen"),("AGF","AGF"),("BIF","Brøndby"),("OB","Odense"),("FCN","Nordsjælland"),("SIF","Silkeborg"),("VB","Vejle BK")])
def test_extractSuperligaTeams_returns_correct_teams(test_input,expected):
    assert util.extractSuperligaTeams(test_input) == expected

def test_extractSuperligaTeams_throws_error_if_team_not_in_list():
    with pytest.raises(ValueError, match=r"Unknown team: Team1"):
        util.extractSuperligaTeams("Team1")


def test_matchTupleToMatchObject_gets_match_object_with_correct_data_from_tuple():
    matchJson = "{\"date\": \"2022-05-22\", \"homeTeam\": \"Chelsea\", \"homeGoals\": 2, \"awayTeam\": \"Watford\", \"awayGoals\": 1, \"homeTeamIsPlayerTeam\": false, \"awayTeamIsPlayerTeam\": false, \"homeTeamIsWinner\": null, \"draw\": false, \"points\": 0}"
    matchTuple = json.loads(matchJson, object_hook = lambda d : namedtuple('Match', d.keys())(*d.values()))
    match = util.matchTupleToMatchObject(matchTuple)
    assert match.date == util.textToDate("2022-5-22")
    assert match.homeTeam == "Chelsea"
    assert match.homeGoals == 2
    assert match.awayGoals == 1
    assert match.awayTeam == "Watford"
        
def test_findTeamByTeamName_finds_team_if_in_list():
    t1 = Team("Team1","player1")
    t2 = Team("Team2","player2")
    t3 = Team("Team3","player3")
    teams = [t1,t2,t3]
    assert util.findTeamByTeamName(teams,"Team1") == t1

def test_findTeamByTeamName_returns_none_if_team_not_in_list():
    t1 = Team("Team1","player1")
    t2 = Team("Team2","player2")
    teams = [t1,t2]
    t3 = Team("Team3","player3")
    with pytest.raises(Exception):
        assert util.findTeamByTeamName(teams,"Team3") == t3

#integration test
def test_getPlayerObjectsFromFile_returns_correct_player_objects_with_correct_data():
    const.FERIEKASSE_NAME = "unitTests/utilTest"
    players = util.getPlayerObjectsFromFile()
    assert len(players) == 2
    assert players[0].name == "player1"
    assert len(players[0].teams) == 2
    assert players[0].teams[0].name == "team1"
    assert players[0].teams[1].name == "team3"
    assert players[1].name == "player2"
    assert len(players[1].teams) == 2
    assert players[1].teams[0].name == "team2"
    assert players[1].teams[1].name == "team4"
    
    
def test_getPlayerThatHasTeam_gets_correct_player_for_team_string():
    player1 = Player("Player1")
    player2 = Player("Player2")
    player3 = Player("Player3")
    player1.teams = [Team("Team1","player1"),Team("Team12","player1"),Team("Team13","player1")]
    player2.teams = [Team("Team2","player2"),Team("Team22","player2"),Team("Team23","player2")]
    player3.teams = [Team("Team3","player3"),Team("Team32","player3"),Team("Team33","player3")]
    players = [player1,player2,player3]
    assert util.getPlayerThatHasTeam("Team1",players) == player1
    assert util.getPlayerThatHasTeam("Team22",players) == player2
    assert util.getPlayerThatHasTeam("Team33",players) == player3
    
def test_getPlayerThatHasTeam_returns_none_if_no_player_has_that_team():
    player1 = Player("Player1")
    player2 = Player("Player2")
    player3 = Player("Player3")
    player1.teams = [Team("Team1","player1"),Team("Team12","player1"),Team("Team13","player1")]
    player2.teams = [Team("Team2","player2"),Team("Team22","player2"),Team("Team23","player2")]
    player3.teams = [Team("Team3","player3"),Team("Team32","player3"),Team("Team33","player3")]
    players = [player1,player2,player3]
    assert util.getPlayerThatHasTeam("Not a real team",players) == None
    
def test_findPlayerObjectInPlayerListFromPlayerName_finds_player_if_in_list():
    player1 = Player("Player1")
    player2 = Player("Player2")
    player3 = Player("Player3")
    players = [player1,player2,player3]
    assert util.findPlayerObjectInPlayerListFromPlayerName("Player1",players) == player1
    
    
def test_findPlayerObjectInPlayerListFromPlayerName_returns_none_if_player_not_in_list():
    player1 = Player("Player1")
    player2 = Player("Player2")
    players = [player1,player2]
    assert util.findPlayerObjectInPlayerListFromPlayerName("Player3",players) == None