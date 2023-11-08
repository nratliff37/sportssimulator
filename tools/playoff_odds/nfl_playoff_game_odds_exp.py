import argparse
import random

# Function Definitions
def play_game(safety):
    home_max = 24
    visit_max = 21 - gb

    for q in range(4):
        home_score = random.randint(0, home_max)
        visit_score = random.randint(0, visit_max)
        print(home_score)
        print(visit_score)

# Main Script
parser = argparse.ArgumentParser()
parser.add_argument('-gb', '--games_behind', help='The number of games behind the visiting team is to the home team.', default=0)
parser.add_argument('-i', '--iterations', help='The number of games to run.', default=1000)
parser.add_argument('--verbose', action=argparse.BooleanOptionalAction, default=False)
parser.add_argument('--safety', action=argparse.BooleanOptionalAction, help='Use if a safety is still in play.', default=False)
#parser.add_argument('-s', '--start', help='Default empty. String that represents the start of a series from the upper team\'s POV (Ex. wlwl)', default="")

args = parser.parse_args()

# Initialize variables
gb = int(args.games_behind)
iterations = int(args.iterations)
verbose = args.verbose
safety = args.safety
#series_start = str(args.start)

# Enter team names
home_team = input("Home Team: ")
visiting_team = input("Visiting Team: ")
win_count = {home_team: 0, visiting_team: 0}

for i in range(iterations):
    play_game(safety)