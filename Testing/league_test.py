import pytest
from classes.League import League
from classes.Team import Team
from classes.Match import Match
import utilities.constants as const
import datetime
import utilities.util as util

def getMockLeagueForFindTeamTests():
    mockLeague = League("eng.1")
    mockLeague.teams.append(Team("name1","player1"))
    mockLeague.teams.append(Team("name2","player2"))
    mockLeague.teams.append(Team("name3","player3"))
    mockLeague.teams.append(Team("name4","player4"))
    mockLeague.teams.append(Team("name5","player5"))
    return mockLeague

def test_filterMatches_filters_matches_not_involving_player_teams():
    myLeague = League("eng.1")
    
    match1 = Match()
    match1.awayTeam = "team1"
    match1.homeTeam = "team2"
    
    match2 = Match()
    match2.awayTeam = "team3"
    match2.homeTeam = "not a real team"
    
    match3 = Match()
    match3.awayTeam = "teamNo"
    match3.homeTeam = "team2"
    
    match4 = Match()
    match4.awayTeam = "noTeam"
    match4.homeTeam = "nah"
    
    team1 = Team("team1","player1")
    team2 = Team("team2","player2")
    team3 = Team("team3","player3")
    
    myLeague.matches.extend([match1,match2,match3,match4])
    myLeague.teams.extend([team1,team2,team3])    
    
    myLeague.filterMatches()
    assert len(myLeague.matches) == 3
    assert myLeague.matches == [match1,match2,match3]

def test_calculatePointsForMatches_calculates_points_correctly():
    myLeague = League("eng.1")
    match1 = Match(None,"team1",1,"team2",1)
    match1.homeTeamIsPlayerTeam = True
    match1.awayTeamIsPlayerTeam = True

    match2 = Match(None,"team3",4,"team4",2)
    match2.homeTeamIsPlayerTeam = True
    match2.awayTeamIsPlayerTeam = False
    
    match3 = Match(None,"team5",3,"team6",0)
    match3.homeTeamIsPlayerTeam = False
    match3.awayTeamIsPlayerTeam = True

    team1 = Team("team1","player1")
    team2 = Team("team2","player2")
    team3 = Team("team3","player3")
    
    myLeague.matches.extend([match1,match2,match3])
    myLeague.teams.extend([team1,team2,team3])
    
    myLeague.calculatePointsForMatches()
    assert match1.points == 10 #draw (5) with multiplier (5*2)
    assert match2.points == 0
    assert match3.points == 20

def test_calculatePointsForMatches_calculates_bonus_points_correctly_for_4_goal_win_rule():
    const.FOUR_GOAL_WIN_RULE = True
    myLeague = League("eng.1")
    match1 = Match(None,"team1",4,"team2",0)
    match1.homeTeamIsPlayerTeam = True
    match1.awayTeamIsPlayerTeam = True

    match2 = Match(None,"germany",7,"brazil",1)
    match2.homeTeamIsPlayerTeam = True
    match2.awayTeamIsPlayerTeam = False
    
    match3 = Match(None,"team6",0,"team3",3)
    match3.homeTeamIsPlayerTeam = False
    match3.awayTeamIsPlayerTeam = True

    team1 = Team("team1","player1")
    team2 = Team("team2","player2")
    germany = Team("germany","player3")
    team3 = Team("team3","player4")
    brazil = Team("brazil","player5")
    team6 = Team("team6","player6")
    
    myLeague.matches.extend([match1,match2,match3])
    myLeague.teams.extend([team1,germany,team3,team2,brazil,team6])
    
    myLeague.calculatePointsForMatches()
    assert match1.bonusPoints == -10 #
    assert match2.bonusPoints == -10
    assert match3.bonusPoints == 0



def test_applyMatchMultipliers_applies_no_multipliers_if_only_1_teams_is_a_player_team():
    myLeague = League("eng.1")
    
    newMatch = Match()
    team1 = Team("team1","player1")
    team2 = Team("team2",None)
    newMatch.homeTeam = "team1"
    newMatch.awayTeam = "team2"
    newMatch.homeTeamIsPlayerTeam = False
    newMatch.awayTeamIsPlayerTeam = True
    newMatch.points = 20
    
    myLeague.teams.append(team1)
    myLeague.teams.append(team2)
        
    myLeague.applyMatchMultipliers(newMatch) 
    assert newMatch.points == 20

def test_applyMatchMultipliers_applies_correct_multiplier_for_both_teams_of_same_player():
    myLeague = League("eng.1")
    
    newMatch = Match()
    team1 = Team("team1","player1")
    team2 = Team("team2","player1")
    newMatch.homeTeam = "team1"
    newMatch.awayTeam = "team2"
    newMatch.homeTeamIsPlayerTeam = True
    newMatch.awayTeamIsPlayerTeam = True
    newMatch.points = 20
    
    myLeague.teams.append(team1)
    myLeague.teams.append(team2)
        
    myLeague.applyMatchMultipliers(newMatch) 
    assert newMatch.points == 0

def test_applyMatchMultipliers_applies_correct_multiplier_for_both_teams_of_different_player():
    myLeague = League("eng.1")
    
    newMatch = Match()
    team1 = Team("team1","player1")
    team2 = Team("team2","player2")
    newMatch.homeTeam = "team1"
    newMatch.awayTeam = "team2"
    newMatch.homeTeamIsPlayerTeam = True
    newMatch.awayTeamIsPlayerTeam = True
    newMatch.points = 20
    
    myLeague.teams.append(team1)
    myLeague.teams.append(team2)
        
    myLeague.applyMatchMultipliers(newMatch) 
    assert newMatch.points == 40

def test_applyMatchMultipliers_applies_correct_multiplier_for_draw_for_superliga_slutspil():
    myLeague = League("eng.1")
    myLeague.name = "superliga"
    
    newMatch = Match()
    team1 = Team("team1","player1")
    team2 = Team("team2","player2")
    newMatch.homeTeam = "team1"
    newMatch.awayTeam = "team2"
    newMatch.draw = True
    newMatch.homeTeamIsPlayerTeam = True
    newMatch.awayTeamIsPlayerTeam = True
    newMatch.date = datetime.date(datetime.datetime.now().year,4,15)
    newMatch.points = 5
    
    myLeague.teams.append(team1)
    myLeague.teams.append(team2)
        
    myLeague.applyMatchMultipliers(newMatch) 
    assert newMatch.points == 10
    
def test_applyMatchMultipliers_applies_correct_multiplier_for_away_win_for_superliga_slutspil():
    myLeague = League("eng.1")
    myLeague.name = "superliga"
    
    newMatch = Match()
    team1 = Team("team1","player1")
    team2 = Team("team2","player2")
    newMatch.homeTeam = "team1"
    newMatch.awayTeam = "team2"
    newMatch.homeTeamIsWinner = False
    newMatch.homeTeamIsPlayerTeam = True
    newMatch.awayTeamIsPlayerTeam = True
    newMatch.date = datetime.date(datetime.datetime.now().year,4,15)
    newMatch.points = 20
    
    myLeague.teams.append(team1)
    myLeague.teams.append(team2)
        
    myLeague.applyMatchMultipliers(newMatch) 
    assert newMatch.points == 40

def test_applyMatchMultipliers_applies_correct_multiplier_for_home_win_for_superliga_slutspil():
    myLeague = League("eng.1")
    myLeague.name = "superliga"
    
    newMatch = Match()
    team1 = Team("team1","player1")
    team2 = Team("team2","player2")
    newMatch.homeTeam = "team1"
    newMatch.awayTeam = "team2"
    newMatch.homeTeamIsWinner = True
    newMatch.homeTeamIsPlayerTeam = True
    newMatch.awayTeamIsPlayerTeam = True
    newMatch.date = datetime.date(datetime.datetime.now().year,4,15)
    newMatch.points = 20
    
    myLeague.teams.append(team1)
    myLeague.teams.append(team2)
        
    myLeague.applyMatchMultipliers(newMatch) 
    assert newMatch.points == 20    
    
def test_applyMatchMultipliers_applies_correct_multiplier_for_home_win_for_superliga_grundspil():
    myLeague = League("eng.1")
    myLeague.name = "superliga"
    
    newMatch = Match()
    team1 = Team("team1","player1")
    team2 = Team("team2","player2")
    newMatch.homeTeam = "team1"
    newMatch.awayTeam = "team2"
    newMatch.homeTeamIsWinner = True
    newMatch.homeTeamIsPlayerTeam = True
    newMatch.awayTeamIsPlayerTeam = True
    newMatch.date = datetime.date(datetime.datetime.now().year,3,15)
    newMatch.points = 20
    
    myLeague.teams.append(team1)
    myLeague.teams.append(team2)
        
    myLeague.applyMatchMultipliers(newMatch) 
    assert newMatch.points == 40    
    
def test_applyMatchMultipliers_applies_correct_multiplier_with_changed_INDBYRDES_MULTIPLIER_constant():
    myLeague = League("eng.1")
    
    newMatch = Match()
    team1 = Team("team1","player1")
    team2 = Team("team2","player2")
    newMatch.homeTeam = "team1"
    newMatch.awayTeam = "team2"
    newMatch.homeTeamIsPlayerTeam = True
    newMatch.awayTeamIsPlayerTeam = True
    newMatch.points = 30
    
    const.INDBYRDES_MULTIPLIER = 3
    
    myLeague.teams.append(team1)
    myLeague.teams.append(team2)
        
    myLeague.applyMatchMultipliers(newMatch) 
    assert newMatch.points == 90

def test_findTeamByTeamName_finds_team_if_it_is_there():
    mockLeague = getMockLeagueForFindTeamTests()
    newTeam = Team("newName","newPlayer")
    mockLeague.teams.append(newTeam)
    assert util.findTeamByTeamName(mockLeague.teams,newTeam.name) == newTeam
    
def test_findTeamByTeamName_raises_exception_if_team_is_not_there():
    mockLeague = getMockLeagueForFindTeamTests()
    newTeamNotThere = Team("raise","exception")
    with pytest.raises(Exception):
        util.findTeamByTeamName(mockLeague.teams,newTeamNotThere.name) == newTeamNotThere

def test_getMatchesOnDate_returns_matches_on_date():
    from datetime import date
    
    myLeague = League("eng.1")
    testDate = date(2025,12,27)
    
    matches = myLeague.getMatchesOnDate(testDate)
    
    assert len(matches) == 7
    
    # Match 1: Nott'ham Forest 1–2 Manchester City
    assert matches[0].date == testDate
    assert matches[0].homeTeam == "Nottingham Forest"
    assert matches[0].homeGoals == 1
    assert matches[0].awayTeam == "Manchester City"
    assert matches[0].awayGoals == 2

    # Match 2: Arsenal 2–1 Brighton
    assert matches[1].date == testDate
    assert matches[1].homeTeam == "Arsenal"
    assert matches[1].homeGoals == 2
    assert matches[1].awayTeam == "Brighton & Hove Albion"
    assert matches[1].awayGoals == 1

    # Match 3: Brentford 4–1 Bournemouth
    assert matches[2].date == testDate
    assert matches[2].homeTeam == "Brentford"
    assert matches[2].homeGoals == 4
    assert matches[2].awayTeam == "AFC Bournemouth"
    assert matches[2].awayGoals == 1

    # Match 4: Burnley 0–0 Everton
    assert matches[3].date == testDate
    assert matches[3].homeTeam == "Burnley"
    assert matches[3].homeGoals == 0
    assert matches[3].awayTeam == "Everton"
    assert matches[3].awayGoals == 0

    # Match 5: Liverpool 2–1 Wolves
    assert matches[4].date == testDate
    assert matches[4].homeTeam == "Liverpool"
    assert matches[4].homeGoals == 2
    assert matches[4].awayTeam == "Wolverhampton Wanderers"
    assert matches[4].awayGoals == 1

    # Match 6: West Ham 0–1 Fulham
    assert matches[5].date == testDate
    assert matches[5].homeTeam == "West Ham United"
    assert matches[5].homeGoals == 0
    assert matches[5].awayTeam == "Fulham"
    assert matches[5].awayGoals == 1

    # Match 7: Chelsea 1–2 Aston Villa
    assert matches[6].date == testDate
    assert matches[6].homeTeam == "Chelsea"
    assert matches[6].homeGoals == 1
    assert matches[6].awayTeam == "Aston Villa"
    assert matches[6].awayGoals == 2
