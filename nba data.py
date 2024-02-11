from requests import get
import json
import time

BASE_URL = "https://cdn.nba.com/"
ALL_JSON = "/static/json/liveData/scoreboard/todaysScoreboard_00.json"
JSON_FILE = "scoreboard.json"


def get_info():
    data = get(BASE_URL + ALL_JSON).json()
    info = data['scoreboard']
    return info

def get_scoreboard():
    while True:

        data = {}
        date = get_info()['gameDate']
        games = get_info()['games']

        for game in games:
            home = game['homeTeam']
            away = game['awayTeam']
            period = game['period']
            gameLeaders = game['gameLeaders']

            homeLeaders = gameLeaders['homeLeaders']
            awayLeaders = gameLeaders['awayLeaders']

            homeLeader_name, homeLeader_pos, homeLeader_points, homeLeader_reb, homeLeader_as = homeLeaders['name'], homeLeaders['position'], homeLeaders['points'], homeLeaders['rebounds'], homeLeaders['assists']
            awayLeader_name, awayLeader_pos, awayLeader_points, awayLeader_reb, awayLeader_as = awayLeaders['name'], awayLeaders['position'], awayLeaders['points'], awayLeaders['rebounds'], awayLeaders['assists']


            game_info = {
                "home_team": home['teamTricode'],
                "away_team": away['teamTricode'],
                "home_score": home['score'],
                "away_score": away['score'],
                "home_leader": {
                    "name": homeLeader_name,
                    "position": homeLeader_pos,
                    "points": homeLeader_points,
                    "rebounds": homeLeader_reb,
                    "assists": homeLeader_as
                },
                "away_leader": {
                    "name": awayLeader_name,
                    "position": awayLeader_pos,
                    "points": awayLeader_points,
                    "rebounds": awayLeader_reb,
                    "assists": awayLeader_as
                },
                "period": period
            }

            data[home['teamTricode'] + "_vs_" + away['teamTricode']] = game_info
            print("------------------------------------------")
            print(f"Day: {date}")
            print(f"{home['teamTricode']} vs. {away['teamTricode']}")
            print(f"{home['score']} - {away['score']}")
            print(f"Home Leader: {homeLeader_name} ({homeLeader_pos}) ({homeLeader_points} POINTS) ({homeLeader_reb} REBOUNDS) ({homeLeader_as} ASSISTS)")
            print(f"Away Leader: {awayLeader_name} ({awayLeader_pos}) ({awayLeader_points} POINTS) ({awayLeader_reb} REBOUNDS) ({awayLeader_as} ASSISTS)")
            print(f"Period - {period}")

        with open(JSON_FILE, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print("Scoreboard updated. Waiting for 5 seconds...")
        time.sleep(5)

if __name__ == "__main__":
    get_scoreboard()
