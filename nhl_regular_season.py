import argparse

TEAMS = {}

# Function Definitions
def create_teams():
    teams_file = open("nhl_teams.txt", "r")

    for team in teams_file:
        team_pair = team.split(", ")
        abv = team_pair[0]
        name = team_pair[1].rstrip('\n')

        TEAMS[abv] = {}
        TEAMS[abv]["name"] = name
        TEAMS[abv]["wins"] = 0
        TEAMS[abv]["losses"] = 0
        TEAMS[abv]["otl"] = 0

    teams_file.close()

def play_game(away_team, home_team):
    print(away_team, home_team)

# Main Script
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--schedule' , help='the text file for the schedule')

try:
    args = parser.parse_args()
    schedule = args.schedule
except:
    print("No schedule given.")
    exit()

# Create the teams
create_teams()

# Read the schedule file and parse through the games
schedule_file = open(schedule, "r")

it = 0
for game in schedule_file:
    if it > 14:
        break

    game_teams = game.split(" @ ")
    away_team = game_teams[0]
    home_team = game_teams[1].rstrip('\n')

    play_game(away_team, home_team)

    it += 1

schedule_file.close()