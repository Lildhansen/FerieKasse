import pytest

import classes.EmailBody as Emailbody
from classes.Player import Player
import utilities.constants as const

def test_TrailingExtraBodyPicker_condition_returns_true_when_player1_is_trailing_player2():
    trailingBodyPicker = Emailbody.TrailingExtraBodyPicker()
    
    player1 = Player("player1")
    player1.totalPoints = 100
    player2 = Player("player2")
    player2.totalPoints = 105
    const.FERIEKASSE_NAME = "unitTests"
    
    players = [player1,player2]
    assert trailingBodyPicker.condition(players) == True


    