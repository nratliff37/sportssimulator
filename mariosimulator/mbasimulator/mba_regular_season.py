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

# Conference data that never gets sorted
EASTERN_CONFERENCE_RAW_DATA = []
WESTERN_CONFERENCE_RAW_DATA = []

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
        TEAMS[abv]["streak"] = "-"
        
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

def update_streak(team, win):
    streak = team["streak"]
    streak_type = streak[0]
    if win:
        if streak_type == "-" or streak_type == "L":
            team["streak"] = "W1"
        else:
            length = int(streak[1:])
            length += 1
            team["streak"] = "W" + str(length)
    else:
        if streak_type == "-" or streak_type == "W":
            team["streak"] = "L1"
        else:
            length = int(streak[1:])
            length += 1
            team["streak"] = "L" + str(length)


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
    update_streak(team_dict, True)

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
    update_streak(team_dict, False)

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

def get_playoff_teams_with_tie(standings):
    sorted_standings = []
    num_teams = len(standings)
    # Sort by win percentage
    unique_pcts_count = {}
    while len(standings):
        team_to_place = {}
        highest_pct = -1.000
        for team in standings:
            pct = team["pct"]
            

            if pct > highest_pct:
                highest_pct = pct
                team_to_place = team
        
        hightest_pct_str = '{:.3f}'.format(highest_pct)
        try:
            unique_pcts_count[hightest_pct_str] += 1
        except:
            unique_pcts_count[hightest_pct_str] = 1

        standings.remove(team_to_place)
        sorted_standings.append(team_to_place)

    filtered_standings = []
    for i in range(len(sorted_standings)): # Should always be 6
        fourth_team = sorted_standings[3]
        team = sorted_standings[i]
        if i < 4:
            # Team currently qualifies for playoffs
            filtered_standings.append(team)
            continue

        fourth_pct = fourth_team["pct"]
        ith_pct = team["pct"]
        if fourth_pct == ith_pct:
            # Team "qualifies" for playoffs on tie
            filtered_standings.append(team)
        else:
            #This team and every team below gets filtered out
            break

    return filtered_standings

def get_combined_h2h_winner(raw_standings, team1_key, team2_key):
    conf_playoff_teams = get_playoff_teams_with_tie(raw_standings)
    team1_h2h_list = HEAD_TO_HEAD[team1_key]
    team2_h2h_list = HEAD_TO_HEAD[team2_key]
    team1_h2h_count = (0, 0)
    team2_h2h_count = (0, 0)
    for team in conf_playoff_teams:
        team_abv = team["abbreviation"]
        team1_against_team = team1_h2h_list[team_abv]
        team2_against_team = team2_h2h_list[team_abv]

        team1_wins_over_team = team1_against_team[0]
        team1_losses_to_team = team1_against_team[1]
        team1_h2h_count = (team1_h2h_count[0] + team1_wins_over_team, team1_h2h_count[1] + team1_losses_to_team)

        team2_wins_over_team = team2_against_team[0]
        team2_losses_to_team = team2_against_team[1]
        team2_h2h_count = (team2_h2h_count[0] + team2_wins_over_team, team2_h2h_count[1] + team2_losses_to_team)

    team1_playoff_h2h_pct = float(team1_h2h_count[0] / (team1_h2h_count[0] + team1_h2h_count[1]))
    team2_playoff_h2h_pct = float(team2_h2h_count[0] / (team2_h2h_count[0] + team2_h2h_count[1]))

    if team1_playoff_h2h_pct > team2_playoff_h2h_pct:
        return team1_key
    elif team1_playoff_h2h_pct < team2_playoff_h2h_pct:
        return team2_key
    else:
        return "Tie"


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

    # 5. Better winning percentage against teams eligible for the playoffs in own conference (ties included)
    conference = team1["conference"]
    raw_standings = []
    other_raw_standings = [] # Only needed if Step 5 remains in a tie
    if conference == "East":
        raw_standings = EASTERN_CONFERENCE_RAW_DATA
        other_raw_standings = WESTERN_CONFERENCE_RAW_DATA
    elif conference == "West":
        raw_standings = WESTERN_CONFERENCE_RAW_DATA
        other_raw_standings = EASTERN_CONFERENCE_RAW_DATA
    else:
        print("ERROR! Invalid conference.")
        raise ValueError("Conference must be \"East\" or \"West\"")

    tiebreak_5_winner = get_combined_h2h_winner(raw_standings, team1_key, team2_key)
    if tiebreak_5_winner == team1_key:
        team_tuple = (team1, team2)
        return team_tuple
    elif tiebreak_5_winner == team2_key:
        team_tuple = (team2, team1)
        return team_tuple

    # 6. Better winning percentage against teams eligible for the playoffs in other conference (ties included)
    tiebreak_6_winner = get_combined_h2h_winner(other_raw_standings, team1_key, team2_key)
    if tiebreak_6_winner == team1_key:
        team_tuple = (team1, team2)
        return team_tuple
    elif tiebreak_6_winner == team2_key:
        team_tuple = (team2, team1)
        return team_tuple
    
    # 7. Better point differential
    team1_diff = team1["point_diff"]
    team2_diff = team2["point_diff"]
    if team1_diff > team2_diff:
        team_tuple = (team1, team2)
        return team_tuple
    elif team1_diff < team2_diff:
        team_tuple = (team2, team1)
        return team_tuple

    # 8. Coin Toss
    coin_toss = random.randint(0, 1)
    if coin_toss:
        team_tuple = (team2, team1)
        return team_tuple
    else:
        team_tuple = (team1, team2)
        return team_tuple

def sort_multi_way_division_winner(teams):
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

    # If division leader stands alone in division mode, return
    pct_count_list = list(unique_pcts_count.values())
    div_leader_pct_count = pct_count_list[0] # Since pcts are sorted
    if div and div_leader_pct_count == 1:
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
            if div:
                tie_broken_teams = break_two_way_tie(team1, team2, div)
                # For division, this is 2 of 3 teams, so we can add the last team to the tie broken
                # teams and return the array
                sorted_standings_after_tie += tie_broken_teams
                sorted_standings_after_tie.append(sorted_standings[2])
                return sorted_standings_after_tie
        elif count > 2:
            tied_teams = []
            for i in range(count):
                team = sorted_standings[team_count]
                tied_teams.append(team)
                team_count += 1
            if div:
                tie_broken_teams = sort_multi_way_division_winner(tied_teams)
                # For division, this can only be 3 teams, so the whole array can be returned
                # once the division winner is determined
                sorted_standings_after_tie += tie_broken_teams
                return sorted_standings_after_tie
        sorted_standings_after_tie += tie_broken_teams


    return sorted_standings_after_tie

def print_standings_section(section_arr):
    team_count = 0
    for team in section_arr:
        name = team["name"]
        wins = str(team["wins"])
        losses = str(team["losses"])
        percentage = team["pct"]

        games_behind_str = "-"
        games_behind = 0.0
        if team_count:
            leader_wins = section_arr[0]["wins"]
            leader_losses = section_arr[0]["losses"]

            wins_int = team["wins"]
            losses_int = team["losses"]

            games_behind = float(((losses_int - leader_losses) + (leader_wins - wins_int)) / 2)
            games_behind_str = '{:.1f}'.format(games_behind) if games_behind else "-"
        
        division_record = str(team["division_wins"]) + "-" + str(team["division_losses"])
        conference_record = str(team["conference_wins"]) + "-" + str(team["conference_losses"])
        point_diff_int = team["point_diff"]
        point_diff = str(point_diff_int) if point_diff_int < 0 else "+" + str(point_diff_int)
        streak = team["streak"]

        team_line =  '{: <4}'.format(str(team_count + 1) + ".") + '{: <26}'.format(name) + '{: <3}'.format(wins) + '{: <3}'.format(losses) + '{:.3f}'.format(percentage) + ' ' + '{: <3}'.format(games_behind_str) + '  '
        team_line += '{: <4}'.format(division_record) + '{: <6}'.format(conference_record) + '{: <5}'.format(point_diff) + '{: <4}'.format(streak)
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
            EASTERN_CONFERENCE_RAW_DATA.append(team_obj)

            if div == "Northeast":
                northeast_division.append(team_obj)
            else:
                southeast_division.append(team_obj)
        else:
            western_conference.append(team_obj)
            WESTERN_CONFERENCE_RAW_DATA.append(team_obj)

            if div == "Northwest":
                northwest_division.append(team_obj)
            else:
                southwest_division.append(team_obj)

    # Next four calls only sort up until the division winner is found
    northeast_division = sort_standings(northeast_division, True)
    southeast_division = sort_standings(southeast_division, True)
    northwest_division = sort_standings(northwest_division, True)
    southwest_division = sort_standings(southwest_division, True)

    eastern_conference = sort_standings(eastern_conference, False)
    western_conference = sort_standings(western_conference, False)
    league = sort_standings(league, False)

    heading = '{: <4}'.format("") + '{: <26}'.format("Team") + '{: <3}'.format("W") + '{: <3}'.format("L") + '{: <6}'.format("PCT") + '{: <5}'.format("GB")
    heading += '{: <4}'.format("DIV") + '{: <6}'.format("CONF") + '{: <5}'.format("DIFF") + '{: <4}'.format("STRK")
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