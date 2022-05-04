import bs4

from utilities.Webdriver import Webdriver as wd
import requests as re
import time

#https://stackoverflow.com/questions/45448994/wait-page-to-load-before-getting-data-with-requests-get-in-python-3

leagueDict = {"premier-league": "https://www.google.com/search?q=premier+league+results&oq=premi&aqs=chrome.1.69i57j35i39l2j46i131i433i512j0i433i512j69i60l2j69i61.1879j1j7&sourceid=chrome&ie=UTF-8#sie=lg;/g/11p44qhs93;2;/m/02_tc;st;fp;1;;",
    "Bundesliga": "https://www.google.com/search?q=bundesliga+resultats&oq=bundes&aqs=chrome.1.69i57j35i39j46i131i433i512l2j0i3j46i512j0i512j0i3l2j46i199i433i465i512.2630j1j9&sourceid=chrome&ie=UTF-8#sie=lg;/g/11m__0kr76;2;/m/037169;st;fp;1;;",
    "laliga": "https://www.google.com/search?q=la+liga+resultats&oq=la+liga+resultats&aqs=chrome..69i57j0i22i30l9.8524j1j9&sourceid=chrome&ie=UTF-8#sie=lg;/g/11mqlmppsd;2;/m/09gqx;st;fp;1;;",
    "serie-a": "https://www.google.com/search?q=serie+a+results&oq=serie+a+results&aqs=chrome..69i57j0i512l2j0i22i30l7.3171j1j9&sourceid=chrome&ie=UTF-8#sie=lg;/g/11n0vx7n5d;2;/m/03zv9;st;fp;1;;",
    "Superliga": "https://www.google.com/search?q=superliga+results&oq=superliga+re&aqs=chrome.1.69i57j35i39l2j0i512l3j69i60l2.3474j1j9&sourceid=chrome&ie=UTF-8#sie=lg;/g/11nmr_75gx;2;/m/06bxjb;st;fp;1;;"}

wd = wd()

for league,link in leagueDict.items():
    if league == "Superliga":
        pass
        #do something else
    else:
        browser = wd.findLeagueUrl(f"{league} results",True)
        time.sleep(2)
        html = wd.driver.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        print(soup)
        a = soup.findall("tr", {"class": "imso-loa imso-hov"})
        wd.quit()
        # scoreLink = re.get(link)
        # scoreLink.raise_for_status()
        # Pi_file = open("WeLovePie.txt","wb")
        # for chunk in scoreLink.iter_content(100000):
        #     Pi_file.write(chunk)
        # print(Pi_file)
        # time.sleep(1)
        # soup = bs4.BeautifulSoup(scoreLink.text,"html.parser")
        # elems = soup.find_all("tr", {"class": "imso-loa imso-hov"})
        # print(len(elems))

#get links for all leagues (to begin with i can just hardcode them in)
#for all leagues
    #get all team names

#store in json object
    #kinda like this:
        #[{"pl": "lfc"}, {"pl": "arsenal"}, {"pl": "chelsea"}]
        
        
#pl : https://www.google.com/search?q=premier+league+results&oq=premi&aqs=chrome.1.69i57j35i39l2j46i131i433i512j0i433i512j69i60l2j69i61.1879j1j7&sourceid=chrome&ie=UTF-8#sie=lg;/g/11p44qhs93;2;/m/02_tc;st;fp;1;;
#laliga : https://www.google.com/search?q=la+liga+resultats&oq=la+liga+resultats&aqs=chrome..69i57j0i22i30l9.8524j1j9&sourceid=chrome&ie=UTF-8#sie=lg;/g/11mqlmppsd;2;/m/09gqx;st;fp;1;;