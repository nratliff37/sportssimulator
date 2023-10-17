import argparse

# Function Definitions
def get_sequences():
    sequence_file = open("series_sequences_" + str(games) + ".txt", "r")
    sequences = []

    for sequence in sequence_file:
        sequence_modified = sequence.rstrip('\n')
        sequences.append(sequence_modified)

    return sequences

def filter_sequences(num_games):
    filtered_sequences = []

    if num_games < (int(games / 2) + 1) or num_games > games:
        print("Invalid number of games.")
        return []

    for sequence in SEQUENCE_LIST:
        if len(sequence) == num_games:
            filtered_sequences.append(sequence)

    return filtered_sequences

def is_home(game_num):
    if games == 7:
        return game_num == 1 or game_num == 2 or (game_num == 5 and not mlb) or (game_num == 6 and mlb) or game_num == 7
    elif games == 5:
        return game_num == 1 or game_num == 2 or game_num == 5
    else:
        return mlb or game_num != 2

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
        for game in range(0, len(sequence)):
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

def validate_start(series_start):
    w_count = 0
    l_count = 0

    for game_result in series_start:
        if game_result == "w":
            w_count += 1
        elif game_result == "l":
            l_count += 1
        else:
            return False

    if w_count > int(games / 2) or l_count > int(games / 2):
        return False
    else:
        return True

def count_losses(series_start):
    l_count = 0

    for game_result in series_start:
        if game_result == "l":
            l_count += 1

    return l_count

def filter_sequences_with_start(num_games, series_start):
    filtered_sequences = []

    if num_games < int(games / 2 + 1) or num_games > games:
        print("Invalid number of games.")
        return []

    for sequence in SEQUENCE_LIST:
        correct_num_games = (len(sequence) == num_games)
        
        start_length = len(series_start)
        sequence_start = sequence[:start_length]
        correct_start = (sequence_start == series_start)

        if correct_num_games and correct_start:
            filtered_sequences.append(sequence)

    return filtered_sequences

def calculate_odds_with_start(num_games, series_start):
    l_count = count_losses(series_start)

    if (int(games / 2 + 1) + l_count) > num_games:
        return 0

    decimal_odds = higher_odds / 100
    home_odds = decimal_odds

    decimal_odds = lower_odds / 100
    away_odds = 1 - decimal_odds
    
    home_odds = round(home_odds, 2)
    away_odds = round(away_odds, 2)

    sequences = filter_sequences_with_start(num_games, series_start)

    final_odds = 0

    start_game = len(series_start)
    for sequence in sequences:
        sequence_odds = 1
        for game in range(start_game, len(sequence)):
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
parser.add_argument('-u', '--upper', help='upper seed odds of winning at home.', default=50)
parser.add_argument('-l', '--lower', help='lower seed odds of winning at home.', default=50)
parser.add_argument('--verbose', action=argparse.BooleanOptionalAction, default=False)
parser.add_argument('-g', '--games', help='Default 7. Input 3, 5, or 7 for the Best of X series odds.', default=7)
parser.add_argument('--mlb', action=argparse.BooleanOptionalAction, help='Use to calculate the odds with a 2-3-2 sequence for 7 games, and a higher seed homestand for 3 games.', default=False)
parser.add_argument('-s', '--start', help='Default empty. String that represents the start of a series from the upper team\'s POV (Ex. wlwl)', default="")

args = parser.parse_args()

# Initialize variables
higher_odds = int(args.upper)
lower_odds = int(args.lower)
verbose = int(args.verbose)
games = int(args.games)
mlb = args.mlb
series_start = str(args.start)

if games == 7:
    ODDS_IN_4 = 0
    ODDS_IN_5 = 0
    ODDS_IN_6 = 0
    ODDS_IN_7 = 0
    SEQUENCE_LIST = get_sequences()
    if not len(series_start):
        ODDS_IN_4 = calculate_odds(4)
        ODDS_IN_5 = calculate_odds(5)
        ODDS_IN_6 = calculate_odds(6)
        ODDS_IN_7 = calculate_odds(7)   
    else:
        valid_start = validate_start(series_start)

        if not valid_start:
            print("Given Series Start was not valid. Must contain w\'s and l\'s only and cannot contain more than 3 of each.")
            exit()

        ODDS_IN_4 = calculate_odds_with_start(4, series_start)
        ODDS_IN_5 = calculate_odds_with_start(5, series_start)
        ODDS_IN_6 = calculate_odds_with_start(6, series_start)
        ODDS_IN_7 = calculate_odds_with_start(7, series_start)

    ODDS_TO_WIN = ODDS_IN_4 + ODDS_IN_5 + ODDS_IN_6 + ODDS_IN_7
    ODDS_TO_WIN = round(ODDS_TO_WIN, 2)

    print(str(ODDS_IN_4) + "% chance of winning in 4 games")
    print(str(ODDS_IN_5) + "% chance of winning in 5 games")
    print(str(ODDS_IN_6) + "% chance of winning in 6 games")
    print(str(ODDS_IN_7) + "% chance of winning in 7 games")
    print(str(ODDS_TO_WIN) + "% chance of winning the series")
elif games == 5:
    pass
elif games == 3:
    pass
else:
    print("Games must be 3, 5, or 7.")
