import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--schedule' , help='the text file for the schedule')

try:
    args = parser.parse_args()
    schedule = args.schedule
except:
    print("No schedule given.")
    exit()

schedule_file = open(schedule, "r")