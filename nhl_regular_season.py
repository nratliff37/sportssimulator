import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--schedule' , help='the text file for the schedule')

try:
    args = parser.parse_args()
    schedule = args.schedule
except:
    print("No schedule given.")
    exit()

TEAMS = {}

def create_teams():
    teams_file = open("nhl_teams.txt", "r")

    for team in teams_file:
        team_pair = team.split(", ")
        abv = team_pair[0]
        name = team_pair[1].rstrip('\n')

    teams_file.close()

# Read the schedule file and parse through the games
schedule_file = open(schedule, "r")

for x in schedule_file:
    pass

schedule_file.close()

create_teams()
print(TEAMS)