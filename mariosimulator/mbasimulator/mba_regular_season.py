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
        TEAMS[abv]["abbreviation"] = abv
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

def break_two_way_tie(team1, team2, div):
    # 1. Better winning percentage in games against each other
    team1_key = team1["abbreviation"]
    team2_key = team2["abbreviation"]
    team1_h2h = HEAD_TO_HEAD[team1_key][team2_key]

    team1_wins, team1_losses = team1_h2h[0], team1_h2h[1]

    if team1_wins > team1_losses:
        team_tuple = (team1, team2)
        return team_tuple
    elif team1_wins < team1_losses:
        team_tuple = (team2, team1)
        return team_tuple

    if not div:
        # 2. Division Leader wins a tie over a team not leading a division
        pass
    else:
        # 3. Division won-lost percentage
        team1_div_pct, team2_div_pct = team1["division_pct"], team2["division_pct"]
        if team1_div_pct > team2_div_pct:
            team_tuple = (team1, team2)
            return team_tuple
        elif team1_div_pct < team2_div_pct:
            team_tuple = (team2, team1)
            return team_tuple

    # 4. Conference won-lost percentage
    team1_conf_pct, team2_conf_pct = team1["conference_pct"], team2["conference_pct"]
    if team1_conf_pct > team2_conf_pct:
        team_tuple = (team1, team2)
        return team_tuple
    elif team1_conf_pct < team2_conf_pct:
        team_tuple = (team2, team1)
        return team_tuple

    team_tuple = (team1, team2)
    return team_tuple

def break_multi_way_tie(teams, div):
    return teams

def sort_standings(unsorted_standings, div):
    sorted_standings = []
    num_teams = len(unsorted_standings)
    # Sort by win percentage
    unique_pcts_count = {}
    while len(unsorted_standings):
        team_to_place = {}
        highest_pct = -1.000
        for team in unsorted_standings:
            pct = team["pct"]
            

            if pct > highest_pct:
                highest_pct = pct
                team_to_place = team
        
        hightest_pct_str = '{:.3f}'.format(highest_pct)
        try:
            unique_pcts_count[hightest_pct_str] += 1
        except:
            unique_pcts_count[hightest_pct_str] = 1

        unsorted_standings.remove(team_to_place)
        sorted_standings.append(team_to_place)

    if len(unique_pcts_count) == num_teams:
        return sorted_standings

    sorted_standings_after_tie = []
    # Determine teams that are tied and break the tie
    team_count = 0
    for pct in unique_pcts_count:
        count = unique_pcts_count[pct]

        tie_broken_teams = []
        if count == 1:
            team = sorted_standings[team_count]
            team_count += 1
            tie_broken_teams.append(team)
        elif count == 2:
            team1 = sorted_standings[team_count]
            team2 = sorted_standings[team_count + 1]
            team_count += 2
            tie_broken_teams = break_two_way_tie(team1, team2, div)
        elif count > 2:
            tied_teams = []
            for i in range(count):
                team = sorted_standings[team_count]
                tied_teams.append(team)
                team_count += 1
            tie_broken_teams = break_multi_way_tie(tied_teams, div)
        sorted_standings_after_tie += tie_broken_teams


    return sorted_standings_after_tie

def print_standings_section(section_arr):
    team_count = 0
    for team in section_arr:
        name = team["name"]
        wins = str(team["wins"])
        losses = str(team["losses"])
        percentage = team["pct"]
        games_behind = '{:.1f}'.format(0) if team_count else "-"
        division_record = str(team["division_wins"]) + "-" + str(team["division_losses"])
        conference_record = str(team["conference_wins"]) + "-" + str(team["conference_losses"])
        point_diff_int = team["point_diff"]
        point_diff = str(point_diff_int) if point_diff_int < 0 else "+" + str(point_diff_int)

        team_line =  '{: <4}'.format(str(team_count + 1) + ".") + '{: <26}'.format(name) + '{: <3}'.format(wins) + '{: <3}'.format(losses) + '{:.3f}'.format(percentage) + ' ' + '{: <3}'.format(games_behind) + '  '
        team_line += '{: <4}'.format(division_record) + '{: <6}'.format(conference_record) + '{: <5}'.format(point_diff)
        print(team_line)
        team_count += 1

def print_standings():
    eastern_conference = []
    western_conference = []
    northeast_division = []
    southeast_division = []
    northwest_division = []
    southwest_division = []
    league = []
    for team in TEAMS:
        team_obj = TEAMS[team]
        conf = team_obj["conference"]
        div = team_obj["division"]

        league.append(team_obj)
        if conf == "East":
            eastern_conference.append(team_obj)

            if div == "Northeast":
                northeast_division.append(team_obj)
            else:
                southeast_division.append(team_obj)
        else:
            western_conference.append(team_obj)

            if div == "Northwest":
                northwest_division.append(team_obj)
            else:
                southwest_division.append(team_obj)

    northeast_division = sort_standings(northeast_division, True)
    southeast_division = sort_standings(southeast_division, True)
    northwest_division = sort_standings(northwest_division, True)
    southwest_division = sort_standings(southwest_division, True)
    eastern_conference = sort_standings(eastern_conference, False)
    western_conference = sort_standings(western_conference, False)
    league = sort_standings(league, False)

    heading = '{: <4}'.format("") + '{: <26}'.format("Team") + '{: <3}'.format("W") + '{: <3}'.format("L") + '{: <6}'.format("PCT") + '{: <5}'.format("GB")
    heading += '{: <4}'.format("DIV") + '{: <6}'.format("CONF") + '{: <5}'.format("DIFF")
    if view == "conf":
        print("\nEastern Conference")
        print(heading)
        print_standings_section(eastern_conference)

        print("\nWestern Conference")
        print(heading)
        print_standings_section(western_conference)
    elif view == "div":
        print("\nNortheast")
        print(heading)
        print_standings_section(northeast_division)

        print("\nSoutheast")
        print(heading)
        print_standings_section(southeast_division)

        print("\nNorthwest")
        print(heading)
        print_standings_section(northwest_division)

        print("\nSouthwest")
        print(heading)
        print_standings_section(southwest_division)
        
    elif view == "league":
        print("\nMBA")
        print(heading)
        print_standings_section(league)   

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