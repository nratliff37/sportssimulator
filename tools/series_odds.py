import argparse

higher_odds = 54
lower_odds = 54
verbose = 0

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

def is_home(game_num):
    return game_num == 1 or game_num == 2 or game_num == 5 or game_num == 7

def calculate_odds(num_games):
    decimal_odds = higher_odds / 100
    home_odds = decimal_odds

    decimal_odds = lower_odds / 100
    away_odds = 1 - decimal_odds
    
    home_odds = round(home_odds, 2)
    away_odds = round(away_odds, 2)

    sequences = filter_sequences(num_games)
    #print(sequences)

    final_odds = 0

    for sequence in sequences:
        sequence_odds = 1
        for game in range(0, num_games):
            result = sequence[game]
            game += 1
            
            if is_home(game):
                if result == 'w':
                    sequence_odds *= home_odds
                else:
                    sequence_odds *= (1- home_odds)
            else:
                if result == 'w':
                    sequence_odds *= away_odds
                else:
                    sequence_odds *= (1- away_odds)

        if verbose:
            print(str(sequence_odds * 100) + "% chance of winning with " + sequence + " sequence.")
                

        final_odds += sequence_odds

    final_odds *= 100
    final_odds = round(final_odds, 2)

    return final_odds

# Main Script
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--upper', help='upper seed odds of winning at home')
parser.add_argument('-l', '--lower', help='lower seed odds of winning at home')
parser.add_argument('-v', '--verbose', help='Default false, 1 for true')

try:
    args = parser.parse_args()
    
    higher_odds = int(args.upper)
    lower_odds = int(args.lower)
    verbose = int(args.verbose)
except:
    pass

SEQUENCE_LIST = get_sequences()

ODDS_IN_4 = calculate_odds(4)
ODDS_IN_5 = calculate_odds(5)
ODDS_IN_6 = calculate_odds(6)
ODDS_IN_7 = calculate_odds(7)
ODDS_TO_WIN = ODDS_IN_4 + ODDS_IN_5 + ODDS_IN_6 + ODDS_IN_7
ODDS_TO_WIN = round(ODDS_TO_WIN, 2)

print(str(ODDS_IN_4) + "% chance of winning in 4 games")
print(str(ODDS_IN_5) + "% chance of winning in 5 games")
print(str(ODDS_IN_6) + "% chance of winning in 6 games")
print(str(ODDS_IN_7) + "% chance of winning in 7 games")
print(str(ODDS_TO_WIN) + "% chance of winning the series")