import pytest
from utilities.Soup import Soup
import bs4

def test_matchIsPostponed_returns_true_if_match_is_postponed():
    postponedMatch = '''<tr data-row="68"><th scope="row" class="right " data-stat="gameweek">7</th><td class="left " data-stat="dayofweek" csk="7">Sat</td><td class="left " data-stat="date" csk="20220910"><a href="/en/matches/2022-09-10">2022-09-10</a></td><td class="right " data-stat="start_time" csk="12:30:00"><span class="venuetime" data-venue-time-only="1" data-venue-epoch="1662809400" data-venue-time="12:30">12:30</span> <span class="localtime" data-label="your time">(13:30)</span></td><td class="right " data-stat="home_team"><a href="/en/squads/fd962109/Fulham-Stats">Fulham</a></td><td class="right iz" data-stat="home_xg"></td><td class="center iz" data-stat="score"></td><td class="right iz" data-stat="away_xg"></td><td class="left " data-stat="away_team"><a href="/en/squads/cff3d9bb/Chelsea-Stats">Chelsea</a></td><td class="right iz" data-stat="attendance"></td><td class="left " data-stat="venue">Craven Cottage</td><td class="left iz" data-stat="referee" csk="2022-09-10"></td><td class="left iz" data-stat="match_report"></td><td class="left " data-stat="notes">Match Postponed</td></tr>'''
    bs4Soup = bs4.BeautifulSoup(postponedMatch,"html.parser")
    postponedMatchElement = bs4Soup.find() #finds first element
    soup = Soup()
    assert soup.matchIsPostponed(postponedMatchElement) == True
    
def test_matchIsPostponed_returns_false_if_match_is_postponed():
    #this is a match with the exact same data as the postponed match, except that the 'notes' data-stat is empty
    postponedMatch = '''<tr data-row="68"><th scope="row" class="right " data-stat="gameweek">7</th><td class="left " data-stat="dayofweek" csk="7">Sat</td><td class="left " data-stat="date" csk="20220910"><a href="/en/matches/2022-09-10">2022-09-10</a></td><td class="right " data-stat="start_time" csk="12:30:00"><span class="venuetime" data-venue-time-only="1" data-venue-epoch="1662809400" data-venue-time="12:30">12:30</span> <span class="localtime" data-label="your time">(13:30)</span></td><td class="right " data-stat="home_team"><a href="/en/squads/fd962109/Fulham-Stats">Fulham</a></td><td class="right iz" data-stat="home_xg"></td><td class="center iz" data-stat="score"></td><td class="right iz" data-stat="away_xg"></td><td class="left " data-stat="away_team"><a href="/en/squads/cff3d9bb/Chelsea-Stats">Chelsea</a></td><td class="right iz" data-stat="attendance"></td><td class="left " data-stat="venue">Craven Cottage</td><td class="left iz" data-stat="referee" csk="2022-09-10"></td><td class="left iz" data-stat="match_report"></td><td class="left " data-stat="notes"></td></tr>'''
    bs4Soup = bs4.BeautifulSoup(postponedMatch,"html.parser")
    postponedMatchElement = bs4Soup.find() #finds first element
    soup = Soup()
    assert soup.matchIsPostponed(postponedMatchElement) == False