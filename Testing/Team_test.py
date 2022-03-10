from classes.Team import Team
import pytest

#cannot do tests with webdriver

def getMockTeam(team,league,country):
    testTeam = Team(team,league,country)
    testTeam.url = "" #resets the url
    return testTeam

@pytest.mark.parametrize("input1, input2, input3, expected", [
    ("Ac Milan","serie-a","italien","https://www.flashscore.dk/hold/ac-milan/8Sa8HInO/"),
    ("Frankfurt","Bundesliga","tyskland","https://www.flashscore.dk/hold/frankfurt/8vndvXTk/"),
    ("Fc midtjylland","Superliga","danmark","https://www.flashscore.dk/hold/fc-midtjylland/8GZDmdbB/")])
def test_getURLFromFile_returns_correct_URL_if_team_is_in_file(input1,input2,input3,expected):
    team = getMockTeam(input1,input2,input3)
    assert team.getURLFromFile() == expected 

def test_getURLFromFile_returns_None_if_team_is_not_in_file():
    team = getMockTeam("Ac Milan","serie-a","italien")
    team.name = "not"
    team.league = "a"
    team.country = "real team"
    assert team.getURLFromFile() == None