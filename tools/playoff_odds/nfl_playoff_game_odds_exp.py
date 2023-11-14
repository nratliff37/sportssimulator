import argparse
import random

HOME_WINS = 0
VISIT_WINS = 0

# Function Definitions
def get_quarter_score(score):
    if score == 1:
        return 0
    elif score == 2 or score == 4:
        return 3
    elif score == 5:
        return 6
    else:
        return score
    
def get_quarter_score_safety(score):
    if score == 1:
        return 0
    elif score == 4:
        return 5
    else:
        return score

def play_game(safety):
    global HOME_WINS
    global VISIT_WINS

    if sb:
        home_max = 21
    else:
        home_max = 24
    
    visit_max = 21 - gb

    home_score = 0
    visit_score = 0
    for q in range(4):
        rand_home = random.randint(0, home_max)
        rand_visit = random.randint(0, visit_max)
        
        home_score_q = 0
        if safety:
            home_score_q = get_quarter_score_safety(rand_home)
            if home_score_q == 2 or home_score_q == 5:
                safety = False
        else:
            home_score_q = get_quarter_score(rand_home)
        
        visit_score_q = 0
        if safety:
            visit_score_q = get_quarter_score_safety(rand_visit)
            if visit_score_q == 2 or visit_score_q == 5:
                safety = False
        else:
            visit_score_q = get_quarter_score(rand_visit)

        home_score += home_score_q
        visit_score += visit_score_q

    if home_score == visit_score:
        ot_win = random.randint(0, 1)
        if ot_win:
            visit_score += 6
        else:
            home_score += 6

    if home_score > visit_score:
        HOME_WINS += 1
        if verbose:
            print(home_team + " Wins " + str(home_score) + "-" + str(visit_score))
    elif home_score < visit_score:
        VISIT_WINS += 1
        if verbose:
            print(visiting_team + " Wins " + str(visit_score) + "-" + str(home_score))
    else:
        print("Error. The two teams have the same final score.")
        exit()

# Main Script
parser = argparse.ArgumentParser()
parser.add_argument('-gb', '--games_behind', help='The number of games behind the visiting team is to the home team.', default=0)
parser.add_argument('-i', '--iterations', help='The number of games to run.', default=100000)
parser.add_argument('--verbose', action=argparse.BooleanOptionalAction, default=False)
parser.add_argument('-s', '--safety', action=argparse.BooleanOptionalAction, help='Use if a safety is still in play.', default=False)
parser.add_argument('-sb', '--super_bowl', action=argparse.BooleanOptionalAction, help='Use if this is for the Super Bowl.', default=False)
#parser.add_argument('-s', '--start', help='Default empty. String that represents the start of a series from the upper team\'s POV (Ex. wlwl)', default="")

args = parser.parse_args()

# Initialize variables
gb = int(args.games_behind)
iterations = int(args.iterations)
verbose = args.verbose
use_safety = args.safety
sb = args.super_bowl
#series_start = str(args.start)

# Enter team names
home_team = input("Home Team: ")
visiting_team = input("Visiting Team: ")

for i in range(iterations):
    play_game(use_safety)

home_odds = HOME_WINS / iterations
home_odds *= 100
home_odds = round(home_odds, 2)

visit_odds = VISIT_WINS / iterations
visit_odds *= 100
visit_odds = round(visit_odds, 2)

print(home_team + " has approximately " + str(home_odds) + "% chance of winning")
print(visiting_team + " has approximately " + str(visit_odds) + "% chance of winning")