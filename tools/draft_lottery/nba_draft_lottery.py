import itertools
import random

BALLS = []
LOTTERY_ORDER = []
COMBINATION_MAP = {}
DRAFT_ORDER = []

def get_team_from_num(num):
    team = ""

    if num < 140:
        team = LOTTERY_ORDER[0]
    elif num < 280:
        team = LOTTERY_ORDER[1]
    elif num < 420:
        team = LOTTERY_ORDER[2]
    elif num < 545:
        team = LOTTERY_ORDER[3]
    elif num < 650:
        team = LOTTERY_ORDER[4]
    elif num < 740:
        team = LOTTERY_ORDER[5]
    elif num < 815:
        team = LOTTERY_ORDER[6]
    elif num < 875:
        team = LOTTERY_ORDER[7]
    elif num < 920:
        team = LOTTERY_ORDER[8]
    elif num < 950:
        team = LOTTERY_ORDER[9]
    elif num < 970:
        team = LOTTERY_ORDER[10]
    elif num < 985:
        team = LOTTERY_ORDER[11]
    elif num < 995:
        team = LOTTERY_ORDER[12]
    elif num < 1000:
        team = LOTTERY_ORDER[13]
    else:
        team = "Reroll"
        
    return team

def convert_to_string(num_arr):
    num_string = ""
    for num in num_arr:
        if num < 10:
            num_string += "0"
        num_string += str(num)
        
    return num_string

# Main Script

for i in range(0, 14):
    BALLS.append(i + 1)
    LOTTERY_ORDER.append("Team" + str(i + 1))

comb_num = 0
for comb in itertools.combinations(BALLS, 4):
    comb_string = convert_to_string(comb)
    
    team = get_team_from_num(comb_num)
    comb_num += 1
    
    COMBINATION_MAP[comb_string] = team

while len(DRAFT_ORDER) < 4:
    balls_copy = []
    for ball in BALLS:
        balls_copy.append(ball)
    
    drawn_balls = []
    
    while len(drawn_balls) < 4:
        drawn_ball = random.choice(balls_copy)
        balls_copy.remove(drawn_ball)
        drawn_balls.append(drawn_ball)
    
    drawn_balls.sort()
    drawn_string = convert_to_string(drawn_balls)
    team = COMBINATION_MAP[drawn_string]
    
    if not DRAFT_ORDER.count(team) and team != "Reroll":
        DRAFT_ORDER.append(team)
    
for team in LOTTERY_ORDER:
    if not DRAFT_ORDER.count(team):
        DRAFT_ORDER.append(team)
        
print(DRAFT_ORDER)