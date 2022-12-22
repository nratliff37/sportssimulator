import argparse
import time
import random

TEAMS = {} # The dictionary that keeps track of team records
GAME_RESULTS = [] # The list of every game results that are written to a file, to be checked for head to head tie breaking

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

def add_win(team):
    team_dict = TEAMS[team]
    team_dict["wins"] += 1

def add_loss(team, ot):
    team_dict = TEAMS[team]

    if ot:
        team_dict["otl"] += 1
    else:
        team_dict["losses"] += 1

def play_game(away_team, home_team):
    home_dict = TEAMS[home_team]

    winner_number = random.random()
    ot_number = random.random()
    ot = (ot_number <= 0.231)
    
    if winner_number > 0.54:
        result_str = away_team + " beat " + home_team
        add_win(away_team)
        add_loss(home_team, ot)
    else:
        result_str = home_team + " beat " + away_team
        add_win(home_team)
        add_loss(away_team, ot)

    if ot:
        result_str += " in OT"

    GAME_RESULTS.append(result_str)

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

for game in schedule_file:
    game_teams = game.split(" @ ")
    away_team = game_teams[0]
    home_team = game_teams[1].rstrip('\n')

    play_game(away_team, home_team)

schedule_file.close()

# Write team records to file

time_stamp = time.time()
output_name = "nhl_team_records_" + str(time_stamp) + ".txt"
record_output = open(output_name, "w")

for team in TEAMS:
    team_data = TEAMS[team]

    name = team_data["name"]
    w = team_data["wins"]
    l = team_data["losses"]
    otl = team_data["otl"]
    pts = 2 * w + otl

    record_string = name + ": " + str(w) + "-" + str(l) + "-" + str(otl) + "; " + str(pts) + " PTS"
    record_output.write(record_string)
    record_output.write("\n")

record_output.close()

# Write game results to file
output_name = "nhl_game_results_" + str(time_stamp) + ".txt"
results_output = open(output_name, "w")

for game in GAME_RESULTS:
    results_output.write(game)
    results_output.write("\n")

results_output.close()