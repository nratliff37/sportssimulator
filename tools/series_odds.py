import argparse

# Constants
ODDS = 50
ADVANTAGE = True
LEAGUE = "Hockey"
REAL = True

# Function Definitions
def get_sequences():
    sequence_file = open("series_sequences.txt", "r")
    sequences = []

    for sequence in sequence_file:
        sequence_modified = sequence.rstrip('\n')
        sequences.append(sequence_modified)

    return sequences

def filter_sequences(num_games):
    filtered_sequences = []

    if num_games < 4 or num_games > 7:
        print("Invalid number of games. Must be between 4 and 7.")
        return []

    for sequence in SEQUENCE_LIST:
        if len(sequence) == num_games:
            filtered_sequences.append(sequence)

    return filtered_sequences

def calculate_odds(num_games):
    decimal_odds = ODDS / 100
    home_odds = 0
    away_odds = 0

    if ADVANTAGE:
        home_odds = decimal_odds
        away_odds = 1 - decimal_odds
    else:
        home_odds = 1 - decimal_odds
        away_odds = decimal_odds
    
    home_odds = round(home_odds, 2)
    away_odds = round(away_odds, 2)

    sequences = filter_sequences(num_games)
    print(sequences)

    return 0

# Main Script
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--odds' , help='your odds of winning at home')
parser.add_argument('-a', '--advantage' , help='0 for home advantage, 1 for no advantage')
parser.add_argument('-l', '--league' , help='league to simulate; options are mlb, nba, and nhl')
parser.add_argument('-r', '--real' , help='0 for real league, 1 for mario league')

try:
    args = parser.parse_args()
    
    ODDS = int(args.odds)
    adv = int(args.advantage)
    league = int(args.league)
    real = int(args.real)

    if adv == 1:
        ADVANTAGE = False
    elif not(adv == 0):
        exit()

    if league == "mlb":
        LEAGUE = "Baseball"
    elif league == "nba":
    elif not(league == "nhl"):
        exit()

    if real == 1:
        REAL = False
    elif not(real == 0):
        exit()
except:
    print("Invalid argument. Assuming default values for invalid arguments (o = 50, a = True, l = Hockey, r = True)")

SEQUENCE_LIST = get_sequences()

ODDS_IN_4 = calculate_odds(4)
ODDS_IN_5 = calculate_odds(5)
ODDS_IN_6 = calculate_odds(6)
ODDS_IN_7 = calculate_odds(7)
#ODDS_TO_WIN = ODDS_IN_4 + ODDS_IN_5 + ODDS_IN_6 + ODDS_IN_7

#print(str(ODDS_IN_4) + "% chance of winning in 4 games")
#print(str(ODDS_IN_5) + "% chance of winning in 5 games")
#print(str(ODDS_IN_6) + "% chance of winning in 6 games")
#print(str(ODDS_IN_7) + "% chance of winning in 7 games")
#print(str(ODDS_TO_WIN) + "% chance of winning the series")