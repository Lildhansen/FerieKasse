
import datetime
import requests, json, os


leagues = ["eng.1", "esp.1", "ger.1", "ita.1", "den.1"]

league = "den.1"

url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/teams"
resp = requests.get(url)
data = resp.json()
# print(data)
for team in data.get("sports", [])[0].get("leagues", [])[0].get("teams", []):
    team_name = team.get("team", {}).get("displayName", "Unknown Team")
    print(team_name)

# for league in leagues:
#     yesterday_dt = datetime.date.today() - datetime.timedelta(days=1)
#     date_str = yesterday_dt.strftime('%Y%m%d')
#     url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard?dates={date_str}"
#     resp = requests.get(url)
#     data = resp.json()
#     for event in data.get("events", []):
        
#         competition = event["competitions"][0]
#         if competition["status"]["type"]["state"] != "post":
#             print("Skipping non-completed match")
#             continue

        
#         home = competition["competitors"][0]
#         away = competition["competitors"][1]
#         print(f"{home['team']['displayName']} vs {away['team']['displayName']}: {home['score']} - {away['score']}")
