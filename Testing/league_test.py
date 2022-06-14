import pytest
from classes.League import League
from classes.Team import Team
from classes.Match import Match
import datetime

def getMockLeagueForFindTeamTests():
    mockLeague = League("testName","testCountry")
    mockLeague.teams.append(Team("name1","player1"))
    mockLeague.teams.append(Team("name2","player2"))
    mockLeague.teams.append(Team("name3","player3"))
    mockLeague.teams.append(Team("name4","player4"))
    mockLeague.teams.append(Team("name5","player5"))
    return mockLeague

def test_filterMatches_filters_matches_not_involving_player_teams():
    myLeague = League("league1","country1")
    
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
    myLeague = League("league1","country1")
    match1 = Match([None,"team1",1,"team2",1])
    match1.homeTeamIsPlayerTeam = True
    match1.awayTeamIsPlayerTeam = True

    match2 = Match([None,"team3",4,"team4",2])
    match2.homeTeamIsPlayerTeam = True
    match2.awayTeamIsPlayerTeam = False
    
    match3 = Match([None,"team5",3,"team6",0])
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

def test_applyMatchMultipliers_applies_no_multipliers_if_only_1_teams_is_a_player_team():
    myLeague = League("league1","country1")
    
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
    myLeague = League("league1","country1")
    
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
    myLeague = League("league1","country1")
    
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
    myLeague = League("league1","country1")
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
    myLeague = League("league1","country1")
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
    myLeague = League("league1","country1")
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
    myLeague = League("league1","country1")
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
    
def test_findTeamByTeamName_finds_team_if_it_is_there():
    mockLeague = getMockLeagueForFindTeamTests()
    newTeam = Team("newName","newPlayer")
    mockLeague.teams.append(newTeam)
    assert mockLeague.findTeamByTeamName(newTeam.name) == newTeam
    
def test_findTeamByTeamName_raises_exception_if_team_is_not_there():
    mockLeague = getMockLeagueForFindTeamTests()
    newTeamNotThere = Team("raise","exception")
    with pytest.raises(Exception):
        mockLeague.findTeamByTeamName(newTeamNotThere.name) == newTeamNotThere
