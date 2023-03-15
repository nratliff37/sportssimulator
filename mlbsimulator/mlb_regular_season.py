import argparse
import time
import numpy as np
import random

TEAMS = {} # The dictionary that keeps track of team records
GAME_RESULTS = [] # The list of every game results that are written to a file, to be checked for head to head tie breaking
GAMES_LEFT = 162 * 15

# Function Definitions
def create_teams():
    teams_file = open("mlb_teams.txt", "r")

    team_counter = 0
    for team in teams_file:
        team_pair = team.split(", ")
        abv = team_pair[0]
        name = team_pair[1].rstrip('\n')

        TEAMS[abv] = {}
        TEAMS[abv]["name"] = name
        TEAMS[abv]["wins"] = 0
        TEAMS[abv]["losses"] = 0
        TEAMS[abv]["division_wins"] = 0
        TEAMS[abv]["division_losses"] = 0
        TEAMS[abv]["league_wins"] = 0
        TEAMS[abv]["league_losses"] = 0
        TEAMS[abv]["sequence"] = ""

        league = ""
        region = ""
        if team_counter < 15:
            league = "American"
        else:
            league = "National"

        if team_counter % 15 < 5:
            region = "East"
        elif team_counter % 15 < 10:
            region = "Central"
        else:
            region = "West"

        TEAMS[abv]["league"] = league
        TEAMS[abv]["region"] = region

        team_counter += 1

    teams_file.close()

def add_win(team, div, league):
    team_dict = TEAMS[team]
    team_dict["wins"] += 1

    if div:
        team_dict["division_wins"] += 1

    if league:
        team_dict["league_wins"] += 1
        team_dict["sequence"] += "w"
    else:
        team_dict["sequence"] += "i"

def add_loss(team, div, league):
    team_dict = TEAMS[team]
    team_dict["losses"] += 1

    if div:
        team_dict["division_losses"] += 1

    if league:
        team_dict["league_losses"] += 1
        team_dict["sequence"] += "l"
    else:
        team_dict["sequence"] += "i"

def record_result(winning_team, losing_team):
    winning_team_dict = TEAMS[winning_team]
    losing_team_dict = TEAMS[losing_team]

    winning_league = winning_team_dict["league"]
    losing_league = losing_team_dict["league"]

    winning_region = winning_team_dict["region"]
    losing_region = losing_team_dict["region"]

    league = (winning_league == losing_league)

    if league:
        div = (winning_region == losing_region)
    else:
        div = False

    add_win(winning_team, div, league)
    add_loss(losing_team, div, league)

def get_record(team, abv):
    team_data = TEAMS[team]

    name = team_data["name"]
    w = team_data["wins"]
    l = team_data["losses"]
    div = str(team_data["division_wins"]) + "-" + str(team_data["division_losses"])
    league = str(team_data["league_wins"]) + "-" + str(team_data["league_losses"])

    label = ""
    if abv:
        label = team
    else:
        label = name

    return label + ": " + str(w) + "-" + str(l) + "; DIV: " + div + "; LG: " + league

# Home team is behind by <return_value> games
def get_games_behind(away_team, home_team):
    away_team_dict = TEAMS[away_team]
    home_team_dict = TEAMS[home_team]

    away_team_wins = away_team_dict["wins"]
    away_team_losses = away_team_dict["losses"]
    home_team_wins = home_team_dict["wins"]
    home_team_losses = home_team_dict["losses"]

    return ((away_team_wins - home_team_wins) + (home_team_losses - away_team_losses)) / 2

def play_game(away_team, home_team):
    #time.sleep(1)

    #np.random.seed(int(time.time()))
    winner_number = random.randint(0, 100)
    
    buffer = int(get_games_behind(away_team, home_team))
    threshold = 55 - int(buffer * 0.8)

    if threshold < 15:
        threshold = 15
    if threshold > 85:
        threshold = 85

    if winner_number >= threshold:
        result_str = away_team + " beat " + home_team
        record_result(away_team, home_team)
    else:
        result_str = home_team + " beat " + away_team
        record_result(home_team, away_team)

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
    schedule_file = open(file_path, "r")
except:
    print("Invalid schedule given.")
    exit()

print("Simulating regular season...")
time.sleep(1)
print("This will take approximately 41 minutes")

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
output_name = "mlb_team_records_" + str(time_stamp) + ".txt"
#record_output = open(output_name, "w")

for team in TEAMS:
    record_string = get_record(team, False)
#    record_output.write(record_string)
#    record_output.write("\n")
    print(record_string)

#record_output.close()

# Write game results to file
output_name = "mlb_game_results_" + str(time_stamp) + ".txt"
#results_output = open(output_name, "w")

#for game in GAME_RESULTS:
#    results_output.write(game)
#    results_output.write("\n")

#results_output.close()
