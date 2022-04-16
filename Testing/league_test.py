import pytest
from classes.League import League
from classes.Team import Team
from classes.Match import Match

def getMockLeagueForFindTeamTests():
    mockLeague = League("testName","testCountry")
    mockLeague.teams.append(Team("name1","player1"))
    mockLeague.teams.append(Team("name2","player2"))
    mockLeague.teams.append(Team("name3","player3"))
    mockLeague.teams.append(Team("name4","player4"))
    mockLeague.teams.append(Team("name5","player5"))
    return mockLeague

#filter matches

#calculatePointsForMatches - en integrationTest:
    #tester at den kan regne point og så lave multiplier
    

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
