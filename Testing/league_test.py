import pytest
from classes.League import League
from classes.Teams import Team

def getMockLeagueForFindTeamTests():
    mockLeague = League("testName","testCountry")
    mockLeague.teams.append(Team("name1","player1"))
    mockLeague.teams.append(Team("name2","player2"))
    mockLeague.teams.append(Team("name3","player3"))
    mockLeague.teams.append(Team("name4","player4"))
    mockLeague.teams.append(Team("name5","player5"))
    return mockLeague

#filter matches
    #måske calculatePointsForMatches - nok ikke, da den indeholder apply match multiplier og match.calculatePoints (men så er det jo en integrationTest)
#apply match multiplier - check 0 and 2

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
