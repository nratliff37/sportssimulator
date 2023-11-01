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

def get_nth_string(num):
    if num < 1 or num > 14:
        print("Number must be between 1 and 14")
    
    if num == 1:
        return "1st"
    if num == 2:
        return "2nd"
    if num == 3:
        return "3rd"
    else:
        return str(num) + "th"

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
        
# Announce the order
print(DRAFT_ORDER)
announce_num = 14
expected_team_num = 13
TOP_FOUR = []
while announce_num > 0:
    nth_string = get_nth_string(announce_num)
    announce_num -= 1
    
    announce_team = DRAFT_ORDER[announce_num]
    print("The " + nth_string + " pick will go to the " + announce_team)
    
    if announce_num >= 4:
        expected_team = LOTTERY_ORDER[expected_team_num]
        expected_team_num -= 1
        
        if announce_team != expected_team:
            jumpgap = 0
            print(expected_team + " is in the Top 4!")
            while announce_team != expected_team:
                jumpgap += 1
                if jumpgap > 1:
                    print(expected_team + " is ALSO in the Top 4!")
                
                TOP_FOUR.append(expected_team)
                expected_team = LOTTERY_ORDER[expected_team_num]
                expected_team_num -= 1
    else:
        while expected_team_num >= 0:
            expected_team = LOTTERY_ORDER[expected_team_num]
            TOP_FOUR.append(expected_team)
            expected_team_num -= 1
            
print(TOP_FOUR)