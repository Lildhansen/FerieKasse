import pytest

from classes.Match import Match
import utilities.constants as const

def test_Match_initialization_sets_up_properties_correct():
    newMatch = Match()
    assert newMatch.homeTeamIsPlayerTeam == False
    assert newMatch.awayTeamIsPlayerTeam == False
    assert newMatch.homeTeamIsWinner == None
    assert newMatch.draw == False
    assert newMatch.points == 0

@pytest.mark.parametrize("test_input", [(Match(None,"a",15,"b",0)), (Match(None,"a",3,"b",2)),(Match(None,"a",7,"b",1))]) 
def test_setupPointCalculation_sets_bools_correct_for_home_win(test_input):
    test_input.setupPointCalculation()
    assert test_input.homeTeamIsWinner == True

@pytest.mark.parametrize("test_input", [(Match(None,"a",0,"b",17)), (Match(None,"a",0,"b",1)),(Match(None,"a",2,"b",5))]) 
def test_setupPointCalculation_sets_bools_correct_for_away_win(test_input):
    test_input.setupPointCalculation()
    assert test_input.homeTeamIsWinner == False
    
@pytest.mark.parametrize("test_input", [(Match(None,"a",10,"b",10)), (Match(None,"a",0,"b",0)),(Match(None,"a",2,"b",2))]) 
def test_setupPointCalculation_sets_bools_correct_for_draw(test_input):
    test_input.setupPointCalculation()
    assert test_input.homeTeamIsWinner == None
    assert test_input.draw == True

@pytest.mark.parametrize("test_input,expected", [(Match(None,"a",15,"b",1),75),(Match(None,"a",0,"b",1),10),(Match(None,"a",2,"b",5),20),(Match(None,"a",5,"b",2),20)]) 
def test_calculateLoss_calculates_points_correctly_based_on_score_if_game_is_a_loss(test_input,expected):
    assert test_input.calculateLoss() == expected

@pytest.mark.parametrize("test_input,expected", [(Match(None,"a",15,"b",1),80),(Match(None,"a",0,"b",1),15),(Match(None,"a",2,"b",5),25)]) 
def test_calculateLoss_calculates_points_correctly_if_LOSE_POINT_constant_is_changed(test_input,expected):
    const.LOSE_POINTS = 10
    assert test_input.calculateLoss() == expected
    
@pytest.mark.parametrize("test_input,expected", [(Match(None,"a",15,"b",1),145),(Match(None,"a",0,"b",1),15),(Match(None,"a",2,"b",5),35)]) 
def test_calculateLoss_calculates_points_correctly_if_POINTS_PER_GOAL_constant_is_changed(test_input,expected):
    const.POINTS_PER_GOAL = 10
    assert test_input.calculateLoss() == expected

@pytest.mark.parametrize("test_input,expected", [(Match(None,"a",15,"b",1),155),(Match(None,"a",0,"b",1),25),(Match(None,"a",2,"b",5),45)]) 
def test_calculateLoss_calculates_points_correctly_if_POINTS_PER_GOAL_AND_LOSE_POINTS_constants_are_changed(test_input,expected):
    const.POINTS_PER_GOAL = 10
    const.LOSE_POINTS = 15
    assert test_input.calculateLoss() == expected
    
@pytest.mark.parametrize("test_input,expected", [(Match(None,"a",0,"b",0),5),(Match(None,"a",7,"b",7),5),(Match(None,"a",2,"b",5),20),(Match(None,"a",10,"b",0),55)])    
def test_calculatePoints_calculates_points_for_matches_correctly_by_score(test_input,expected):
    test_input.setupPointCalculation() #needs to be done - so the flags are correctly set for calculate
    assert test_input.calculate() == expected

def test_calculatePoints_calculate_draws_correctly_if_DRAW_POINTS_constant_is_changed():
    const.DRAW_POINTS = 35
    match = Match(None,"a",0,"b",0)
    match.setupPointCalculation() #needs to be done - so the flags are correctly set for calculate
    assert match.calculate() == 35

def test_points_set_to_0_in_calculatePoints_if_player_team_won():
    homeTeamWinnerMatch = Match(None,"a",1,"b",0)
    homeTeamWinnerMatch.homeTeamIsWinner = True
    assert homeTeamWinnerMatch.points == 0
    
    awayTeamWinnerMatch = Match(None,"a",0,"b",1)
    awayTeamWinnerMatch.awayTeamIsPlayerTeam = True
    assert awayTeamWinnerMatch.points == 0