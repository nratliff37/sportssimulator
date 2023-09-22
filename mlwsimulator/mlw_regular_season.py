import argparse
import time
import numpy as np
import random

TEAMS = {} # The dictionary that keeps track of team records
GAME_RESULTS = [] # The list of every game results that are written to a file, to be checked for head to head tie breaking
GAMES_LEFT = 0

# Function Definitions
def create_teams():
    teams_file = open("mlw_teams.txt", "r")

    for team in teams_file:
        team_pair = team.split(", ")
        abv = team_pair[0]
        name = team_pair[1].rstrip('\n')

        TEAMS[abv] = {}
        TEAMS[abv]["name"] = name
        TEAMS[abv]["wins"] = 0
        TEAMS[abv]["losses"] = 0

    teams_file.close()

def add_win(team):
    team_dict = TEAMS[team]
    team_dict["wins"] += 1

def add_loss(team):
    team_dict = TEAMS[team]

    team_dict["losses"] += 1

def get_record(team, abv):
    team_data = TEAMS[team]

    name = team_data["name"]
    w = team_data["wins"]
    l = team_data["losses"]

    label = ""
    if abv:
        label = team
    else:
        label = name

    return label + ": " + str(w) + "-" + str(l)

def play_game(away_team, home_team):
    time.sleep(1)

    np.random.seed(int(time.time()))
    winner_number = np.random.randint(0, 100)

    if winner_number >= 50:
        result_str = away_team + " beat " + home_team
        add_win(away_team)
        add_loss(home_team)
    else:
        result_str = home_team + " beat " + away_team
        add_win(home_team)
        add_loss(away_team)

    away_record = get_record(away_team, True)
    home_record = get_record(home_team, True)

    home_str = " (" + away_record + ")"
    away_str = "(" + home_record + ")"

    result_str += home_str
    result_str += away_str

    print(result_str)
    GAME_RESULTS.append(result_str)

# Main Script
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--schedule' , help='the text file for the schedule in the format YYYY (i.e 2023)')

try:
    args = parser.parse_args()
    schedule = args.schedule
except:
    print("No schedule given.")
    exit()

# Create the teams
create_teams()

# Read the schedule file and parse through the games
try:
    file_path = ".\schedules\\" + schedule + ".txt"
    schedule_file = open(file_path, "r", encoding='utf-8-sig')
except:
    print("Invalid schedule given.")
    exit()

print("Simulating regular season...")
time.sleep(1)
print("This will take approximately 1 minute")

GAMES_LEFT = 60
for game in schedule_file:
    game_teams = game.split(" @ ")
    away_team = game_teams[0]
    home_team = game_teams[1].rstrip('\n')

    play_game(away_team, home_team)

schedule_file.close()

# Write team records to file

time_stamp = time.time()
output_name = "mlw_team_records_" + str(time_stamp) + ".txt"
record_output = open(output_name, "w")

for team in TEAMS:
    record_string = get_record(team, False)
    record_output.write(record_string)
    record_output.write("\n")
    print(record_string)

record_output.close()

# Write game results to file
output_name = "mlw_game_results_" + str(time_stamp) + ".txt"
results_output = open(output_name, "w")

for game in GAME_RESULTS:
    results_output.write(game)
    results_output.write("\n")

results_output.close()
