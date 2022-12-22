import argparse
import time
import numpy as np
import random

TEAMS = {} # The dictionary that keeps track of team records
GAME_RESULTS = [] # The list of every game results that are written to a file, to be checked for head to head tie breaking
GAMES_LEFT = 0

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

def get_record(team, abv):
    team_data = TEAMS[team]

    name = team_data["name"]
    w = team_data["wins"]
    l = team_data["losses"]
    otl = team_data["otl"]
    pts = 2 * w + otl

    label = ""
    if abv:
        label = team
    else:
        label = name

    return label + ": " + str(w) + "-" + str(l) + "-" + str(otl) + "; " + str(pts) + " PTS"

def play_game(away_team, home_team):
    time.sleep(1)

    np.random.seed(int(time.time()))
    winner_number = np.random.randint(0, 100)
    ot_number = np.random.randint(0, 5)
    ot = (ot_number == 4)
    
    if winner_number >= 54:
        result_str = away_team + " beat " + home_team
        add_win(away_team)
        add_loss(home_team, ot)
    else:
        result_str = home_team + " beat " + away_team
        add_win(home_team)
        add_loss(away_team, ot)

    if ot:
        result_str += " in OT"

    away_record = get_record(away_team, True)
    home_record = get_record(home_team, True)

    home_str = " (" + away_record + ")"
    away_str = "(" + home_record + ")"

    result_str += home_str
    result_str += away_str

    print(result_str)
    GAME_RESULTS.append(result_str)

# Main Script
print("Simulating regular season...")
time.sleep(1)
print("This will take approximately 22 minutes")
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

GAMES_LEFT = 82 * 16
for game in schedule_file:
    game_teams = game.split(" @ ")
    away_team = game_teams[0]
    home_team = game_teams[1].rstrip('\n')

    play_game(away_team, home_team)

    GAMES_LEFT -= 1
    if GAMES_LEFT % 60 == 0:
        minutes_left = int(GAMES_LEFT / 60)

        if minutes_left > 1:
            print(str(minutes_left) + " minutes remaining.")
        elif minutes_left == 1:
            print(str(minutes_left) + " minute remaining.")

schedule_file.close()

# Write team records to file

time_stamp = time.time()
output_name = "nhl_team_records_" + str(time_stamp) + ".txt"
record_output = open(output_name, "w")

for team in TEAMS:
    record_string = get_record(team, False)
    record_output.write(record_string)
    record_output.write("\n")
    print(record_string)

record_output.close()

# Write game results to file
output_name = "nhl_game_results_" + str(time_stamp) + ".txt"
results_output = open(output_name, "w")

for game in GAME_RESULTS:
    results_output.write(game)
    results_output.write("\n")

results_output.close()