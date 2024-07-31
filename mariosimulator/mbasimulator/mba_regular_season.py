import argparse
import time
import numpy as np
import random
import os
import sys

TEAMS = {} # The dictionary that keeps track of team records
GAME_RESULTS = [] # The list of every game results that are written to a file, to be checked for head to head tie breaking
GAMES_LEFT = 0
HEAD_TO_HEAD = {}

# Function Definitions
def create_teams():
    teams_file = open("mba_teams.txt", "r")

    team_counter = 0
    for team in teams_file:
        team_pair = team.split(", ")
        abv = team_pair[0]
        name = team_pair[1].rstrip('\n')

        TEAMS[abv] = {}
        TEAMS[abv]["name"] = name

        conference = ""
        division = ""
        if team_counter < 6:
            conference = "East"
        else:
            conference = "West"

        if team_counter < 3:
            division = "Northeast"
        elif team_counter < 6:
            division = "Southeast"
        elif team_counter < 9:
            division = "Northwest"
        else:
            division = "Southwest"
        TEAMS[abv]["conference"] = conference
        TEAMS[abv]["division"] = division

        TEAMS[abv]["wins"] = 0
        TEAMS[abv]["losses"] = 0
        TEAMS[abv]["pct"] = 0.000
        TEAMS[abv]["conference_wins"] = 0
        TEAMS[abv]["conference_losses"] = 0
        TEAMS[abv]["conference_pct"] = 0.000
        TEAMS[abv]["division_wins"] = 0
        TEAMS[abv]["division_losses"] = 0
        TEAMS[abv]["division_pct"] = 0.000
        TEAMS[abv]["point_diff"] = 0
        
        team_counter += 1

    for team1 in TEAMS:
        HEAD_TO_HEAD[team1] = {}
        for team2 in TEAMS:
            HEAD_TO_HEAD[team1][team2] = (0, 0)

    teams_file.close()

def update_percentages(team, div, conf):
    w, l = team["wins"], team["losses"]
    team["pct"] = float(w / (w + l))

    if conf:
        conf_w, conf_l = team["conference_wins"], team["conference_losses"]
        team["conference_pct"] = float(conf_w / (conf_w + conf_l))

        if div:
            div_w, div_l = team["division_wins"], team["division_losses"]
            team["division_pct"] = float(div_w / (div_w + div_l))

def add_win(team, other_team, div, conf, diff):
    team_dict = TEAMS[team]
    team_dict["wins"] += 1

    if div:
        team_dict["division_wins"] += 1

    if conf:
        team_dict["conference_wins"] += 1

    team_dict["point_diff"] += diff

    h2h_tuple = HEAD_TO_HEAD[team][other_team]
    h2h_tuple_list = list(h2h_tuple)
    h2h_tuple_list[0] += 1
    h2h_updated_tuple = tuple(h2h_tuple_list)
    HEAD_TO_HEAD[team][other_team] = h2h_updated_tuple

    update_percentages(team_dict, div, conf)

def add_loss(team, other_team, div, conf, diff):
    team_dict = TEAMS[team]
    team_dict["losses"] += 1

    if div:
        team_dict["division_losses"] += 1

    if conf:
        team_dict["conference_losses"] += 1

    team_dict["point_diff"] -= diff

    h2h_tuple = HEAD_TO_HEAD[team][other_team]
    h2h_tuple_list = list(h2h_tuple)
    h2h_tuple_list[1] += 1
    h2h_updated_tuple = tuple(h2h_tuple_list)
    HEAD_TO_HEAD[team][other_team] = h2h_updated_tuple

    update_percentages(team_dict, div, conf)

def record_result(winning_team, losing_team, point_diff):
    winning_team_dict = TEAMS[winning_team]
    losing_team_dict = TEAMS[losing_team]

    winning_conf = winning_team_dict["conference"]
    losing_conf = losing_team_dict["conference"]

    winning_div = winning_team_dict["division"]
    losing_div = losing_team_dict["division"]

    conf = (winning_conf == losing_conf)

    if conf:
        div = (winning_div == losing_div)
    else:
        div = False

    add_win(winning_team, losing_team, div, conf, point_diff)
    add_loss(losing_team, winning_team, div, conf, point_diff)

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
    if not test:
        np.random.seed(int(time.time()))
        winner_number = np.random.randint(0, 100)
    else:
        winner_number = random.randint(0, 99)
    
    if winner_number >= 50:
        result_str = away_team + " beat " + home_team
        point_diff = winner_number - 50 + 1
        record_result(away_team, home_team, point_diff)
    else:
        result_str = home_team + " beat " + away_team
        point_diff = 50 - winner_number
        record_result(home_team, away_team, point_diff)

    away_record = get_record(away_team, True)
    home_record = get_record(home_team, True)

    home_str = " (" + away_record + ")"
    away_str = "(" + home_record + ")"

    result_str += home_str
    result_str += away_str

    print(result_str)
    GAME_RESULTS.append(result_str)

def print_standings():
    eastern_conference = []
    western_conference = []
    for team in TEAMS:
        team_obj = TEAMS[team]
        conf = team_obj["conference"]

        if conf == "East":
            eastern_conference.append(team_obj)
        else:
            western_conference.append(team_obj)

    # TODO
    # SORT THE STANDINGS

    if view == "conf":
        print("\nEastern Conference")
        heading = '{: <20}'.format("Team") + '{: <3}'.format("W") + '{: <3}'.format("L") + '{: <6}'.format("PCT") + '{: <5}'.format("GB")
        heading += '{: <4}'.format("DIV") + '{: <6}'.format("CONF") + '{: <5}'.format("DIFF")
        print(heading)
        
        for team in eastern_conference:
            name = team["name"]
            wins = str(team["wins"])
            losses = str(team["losses"])
            percentage = team["pct"]
            games_behind = 0.0
            division_record = str(team["division_wins"]) + "-" + str(team["division_losses"])
            conference_record = str(team["conference_wins"]) + "-" + str(team["conference_losses"])
            point_diff = str(team["point_diff"])

            team_line = '{: <20}'.format(name) + '{: <3}'.format(wins) + '{: <3}'.format(losses) + '{:.3f}'.format(percentage) + ' ' + '{:.1f}'.format(games_behind) + '  '
            team_line += '{: <4}'.format(division_record) + '{: <6}'.format(conference_record) + '{: <5}'.format(point_diff)
            print(team_line)

        print("\nWestern Conference")
        print(heading)
        for team in western_conference:
            name = team["name"]
            wins = str(team["wins"])
            losses = str(team["losses"])
            percentage = team["pct"]
            games_behind = 0.0
            division_record = str(team["division_wins"]) + "-" + str(team["division_losses"])
            conference_record = str(team["conference_wins"]) + "-" + str(team["conference_losses"])
            point_diff = str(team["point_diff"])

            team_line = '{: <20}'.format(name) + '{: <3}'.format(wins) + '{: <3}'.format(losses) + '{:.3f}'.format(percentage) + ' ' + '{:.1f}'.format(games_behind) + '  '
            team_line += '{: <4}'.format(division_record) + '{: <6}'.format(conference_record) + '{: <5}'.format(point_diff)
            print(team_line)
    elif view == "div":
        pass
    elif view == "league":
        league = []
        for team in TEAMS:
            team_obj = TEAMS[team]
            league.append(team_obj)

        # TODO
        # SORT THE STANDINGS

        print("\nMBA")
        heading = '{: <20}'.format("Team") + '{: <3}'.format("W") + '{: <3}'.format("L") + '{: <6}'.format("PCT") + '{: <5}'.format("GB")
        heading += '{: <4}'.format("DIV") + '{: <6}'.format("CONF") + '{: <5}'.format("DIFF")
        print(heading)
        
        for team in league:
            name = team["name"]
            wins = str(team["wins"])
            losses = str(team["losses"])
            percentage = team["pct"]
            games_behind = 0.0
            division_record = str(team["division_wins"]) + "-" + str(team["division_losses"])
            conference_record = str(team["conference_wins"]) + "-" + str(team["conference_losses"])
            point_diff = str(team["point_diff"])

            team_line = '{: <20}'.format(name) + '{: <3}'.format(wins) + '{: <3}'.format(losses) + '{:.3f}'.format(percentage) + ' ' + '{:.1f}'.format(games_behind) + '  '
            team_line += '{: <4}'.format(division_record) + '{: <6}'.format(conference_record) + '{: <5}'.format(point_diff)
            print(team_line)        

# Main Script
parser = argparse.ArgumentParser()
parser.add_argument('--test', action=argparse.BooleanOptionalAction, default=False, help="Use this to run in test mode (Runs instantly and skips file writing).")
parser.add_argument('-v', '--view', type=str, default='conf', help="The view to use for standings (conf, div, league).")

try:
    args = parser.parse_args()
    test = args.test
    view = args.view

    if view == "Conference" or view == "Conf":
        view = "conf"
    if view == "Division" or view == "Div":
        view = "div"
    if view == "MBA" or view == "mba" or view == "League":
        view = "league"

    if view != "conf" and view != "div" and view != "league":
        print("Invalid View")
        raise Exception("Invalid View")
except:
    exit()

# Create the teams
create_teams()

# Read the schedule file and parse through the games
file_path = ".\mba_schedule.txt"
schedule_file = open(file_path, "r")

if not test:
    print("Simulating regular season...")
    time.sleep(1)
    print("This will take approximately 4 minutes")

GAMES_LEFT = 32 * 6
for game in schedule_file:
    game_teams = game.split(" @ ")
    away_team = game_teams[0]
    home_team = game_teams[1].rstrip('\n')

    if not test:
        time.sleep(1)
        os.system('cls')
    play_game(away_team, home_team)

    GAMES_LEFT -= 1
    if GAMES_LEFT % 60 == 0 and not test:
        minutes_left = int(GAMES_LEFT / 60)

        if minutes_left > 1:
            print(str(minutes_left) + " minutes remaining.")
        elif minutes_left == 1:
            print(str(minutes_left) + " minute remaining.")

    if not test:
        print_standings()

schedule_file.close()

if not test:
    # Write team records to file
    time_stamp = time.time()
    output_name = "mba_team_records_" + str(time_stamp) + ".txt"
    record_output = open(output_name, "w")

    for team in TEAMS:
        record_string = get_record(team, False)
        record_output.write(record_string)
        record_output.write("\n")
    
    print_standings()
    record_output.close()

    # Write game results to file
    output_name = "mba_game_results_" + str(time_stamp) + ".txt"
    results_output = open(output_name, "w")

    for game in GAME_RESULTS:
        results_output.write(game)
        results_output.write("\n")

    results_output.close()
else:
    for team in TEAMS:
        record_string = get_record(team, False)
    print_standings()