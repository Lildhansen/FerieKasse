import pytest

import classes.EmailBody as Emailbody
from classes.Player import Player
from classes.Team import Team
import utilities.constants as const

def test_TrailingExtraBodyPicker_condition_returns_true_when_player1_is_trailing_player2():
    trailingBodyPicker = Emailbody.TrailingExtraBodyPicker()
    
    player1 = Player("player1")
    player2 = Player("player2")
    const.FERIEKASSE_NAME = "unitTests/extraBodyTrailingTrue"
    
    players = [player1,player2]
    assert trailingBodyPicker.condition(players) == True

def test_TrailingExtraBodyPicker_condition_returns_false_when_player1_is_not_trailing_player2():
    trailingBodyPicker = Emailbody.TrailingExtraBodyPicker()
    
    player1 = Player("player1")
    player2 = Player("player2")
    const.FERIEKASSE_NAME = "unitTests/extraBodyTrailingFalse"
    
    players = [player1,player2]
    assert trailingBodyPicker.condition(players) == False
    
def test_TrailingExtraBodyPicker_condition_returns_false_when_there_is_only_1_player():
    trailingBodyPicker = Emailbody.TrailingExtraBodyPicker()
    
    player1 = Player("player1")
    
    players = [player1]
    assert trailingBodyPicker.condition(players) == False
  
def test_LosingExtraBodyPicker_condition_is_always_true():
    losingBodyPicker = Emailbody.LosingExtraBodyPicker()
    
    player1 = Player("player1")
    player2 = Player("player2")
    const.FERIEKASSE_NAME = "unitTests/extraBodyPlayer"
    
    players = [player1,player2]
    assert losingBodyPicker.condition(players) == True
  
def test_LosingExtraBodyPicker_finds_player_with_most_points():
    losingBodyPicker = Emailbody.LosingExtraBodyPicker()
    
    player1 = Player("player1")
    player2 = Player("player2")
    const.FERIEKASSE_NAME = "unitTests/extraBodyPlayer"
    
    players = [player1,player2]
    losingBodyPicker.condition(players)
    assert losingBodyPicker.playerPoints == 200
    assert losingBodyPicker.mostPointsPlayerName == "player2"

def test_LeadingExtraBodyPicker_condition_is_always_true():
    leadingBodyPicker = Emailbody.LeadingExtraBodyPicker()
    
    player1 = Player("player1")
    player2 = Player("player2")
    const.FERIEKASSE_NAME = "unitTests/extraBodyPlayer"
    
    players = [player1,player2]
    assert leadingBodyPicker.condition(players) == True
  
def test_LeadingExtraBodyPicker_finds_player_with_most_points():
    leadingBodyPicker = Emailbody.LeadingExtraBodyPicker()
    
    player1 = Player("player1")
    player2 = Player("player2")
    const.FERIEKASSE_NAME = "unitTests/extraBodyPlayer"
    
    players = [player1,player2]
    leadingBodyPicker.condition(players)
    assert leadingBodyPicker.playerPoints == 100
    assert leadingBodyPicker.leastPointsPlayerName == "player1"
   
def test_HighestScoreTeamExtraBodyPicker_condition_is_always_true():
    highestTeamBodyPicker = Emailbody.HighestScoreTeamExtraBodyPicker()
    
    player1 = Player("player1")
    player1.teams = [Team("a","player1",""),Team("b","player1","")]
    player2 = Player("player2")
    player2.teams = [Team("c","player2",""),Team("d","player2","")]
    const.FERIEKASSE_NAME = "unitTests/extraBodyTeam"
    
    players = [player1,player2]
    assert highestTeamBodyPicker.condition(players) == True
  
def test_HighestScoreTeamExtraBodyPicker_finds_team_with_most_points():
    highestTeamBodyPicker = Emailbody.HighestScoreTeamExtraBodyPicker()
    
    player1 = Player("player1")
    player1.teams = [Team("a","player1",""),Team("b","player1","")]
    player2 = Player("player2")
    player2.teams = [Team("c","player2",""),Team("d","player2","")]
    const.FERIEKASSE_NAME = "unitTests/extraBodyTeam"
    
    players = [player1,player2]
    highestTeamBodyPicker.condition(players)
    assert highestTeamBodyPicker.teamPoints == 100
    assert highestTeamBodyPicker.mostPointsTeamName == "b"
    assert highestTeamBodyPicker.mostPointsTeamPlayerName == "player1"

def test_LowestScoreTeamExtraBodyPicker_condition_is_always_true():
    lowestTeamBodyPicker = Emailbody.LowestScoreTeamExtraBodyPicker()
    
    player1 = Player("player1")
    player1.teams = [Team("a","player1",""),Team("b","player1","")]
    player2 = Player("player2")
    player2.teams = [Team("c","player2",""),Team("d","player2","")]
    const.FERIEKASSE_NAME = "unitTests/extraBodyTeam"
    
    players = [player1,player2]
    assert lowestTeamBodyPicker.condition(players) == True
  
def test_LeadingExtraBodyPicker_finds_player_with_most_points():
    lowestTeamBodyPicker = Emailbody.LowestScoreTeamExtraBodyPicker()
    
    player1 = Player("player1")
    player1.teams = [Team("a","player1",""),Team("b","player1","")]
    player2 = Player("player2")
    player2.teams = [Team("c","player2",""),Team("d","player2","")]
    const.FERIEKASSE_NAME = "unitTests/extraBodyTeam"
    
    players = [player1,player2]
    lowestTeamBodyPicker.condition(players)
    assert lowestTeamBodyPicker.teamPoints == 10
    assert lowestTeamBodyPicker.leastPointsTeamName == "d"
    assert lowestTeamBodyPicker.leastPointsTeamPlayerName == "player2"
   

    