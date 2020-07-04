import csv
import os
import datetime as dt
import numpy as ny
import sys
import math

# function that creates a CSV file with statistics for each problem
def stats_by_problem(inFileName, outFileName, problemType):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the output file for writing
    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, outFileName), "w")

    # open the input and output files as csv files
    with open(os.path.join(dir, inFileName)) as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # create dictionary that tracks the problems and the time users spend on problems
        probDict = dict()

        # create dictionary that tracks a users completion status of problems and last move
        usersCompletedProb = dict()
        usersAttemptedProb = dict()
        usersLastMove = dict()
        exp1_pp1aTracker = dict()

        # loop through the data
        for cols in csv_reader:

            # get the user, time, move, and problem name
            user = cols[0]
            time = dt.datetime.strptime(cols[1], "%Y-%m-%d %H:%M:%S")
            move = cols[2]
            div = cols[3]

            # if no dictionary for this problem create one and add this user and answer
            if div not in probDict:
                userDict = {}
                probDict[div] = userDict
            else:
                userDict = probDict[div]

            # if user is not in usersCompletedProb or usersAttemptedProb add user
            if user not in usersCompletedProb:
                usersCompletedProb[user] = []
            if user not in usersAttemptedProb:
                usersAttemptedProb[user] = []

            # sets a new user's last move to not available
            if user not in usersLastMove:
                usersLastMove[user] = [div, "start", time]

            # track when user starts a problem and add the timestamp to probDict
            if user not in userDict:

                probDict[div][user] = []
                probDict[div][user].append(time)

                # tracking exp1_pp1a times
                if div == "exp1_pp1a":
                    exp1_pp1aTracker[user] = []
                    exp1_pp1aTracker[user].append(["Start", str(time)])

            # only edits the timestamp if user in already in probDict and the user has started the problem
            elif user in userDict and div not in usersCompletedProb[user]:

                # track the time user is spending on a problem
                if not isinstance(probDict[div][user][len(probDict[div][user]) - 1], str):

                    # ignores the time if the user spends over five minutes on a problem
                    if time - usersLastMove[user][2] > dt.timedelta(minutes=5):

                        # saves the times before the five minutes and appends time after the five minutes
                        probDict[div][user][len(probDict[div][user]) - 1] = str(usersLastMove[user][2] - probDict[div][user][len(probDict[div][user]) - 1])
                        probDict[div][user].append(time)

                        if div == "exp1_pp1a":
                            exp1_pp1aTracker[user].append(["Longer Than 5 Mins", str(usersLastMove[user][2])])

                    # when student gets problem correct, ends the time tracking and adds user to usersCompletedProb
                    if move.split('|')[0] == "correct" or move.split('.')[0] == "percent:100":

                        probDict[div][user][len(probDict[div][user]) - 1] = str(time - probDict[div][user][len(probDict[div][user]) - 1])
                        usersCompletedProb[user].append(div)
                        usersAttemptedProb[user].append(div)

                        if div == "exp1_pp1a":
                            exp1_pp1aTracker[user].append(["Correct", str(time)])

                        for x in range(len(probDict[div][user])):

                            if not isinstance(probDict[div][user][x], str):

                                probDict[div][user].pop(x)

                    elif move.split('|')[0] == "incorrect" or move.split(':')[0] == "percent":

                        usersAttemptedProb[user].append(div)

                # track when students come back to the problem
                elif isinstance(probDict[div][user][len(probDict[div][user]) - 1], str):

                    if move != "differentProblem":

                        probDict[div][user].append(time)
                        if user in exp1_pp1aTracker:
                            exp1_pp1aTracker[user].append(["Came Back to Question", str(time)])

                # track when students move on to a different problem
                if move == "differentProblem":

                    if usersLastMove[user][0] != "differentProblem" and not isinstance(probDict[usersLastMove[user][0]][user][len(probDict[usersLastMove[user][0]][user]) - 1], str):

                        probDict[usersLastMove[user][0]][user][len(probDict[usersLastMove[user][0]][user]) - 1] = str(time - probDict[usersLastMove[user][0]][user][len(probDict[usersLastMove[user][0]][user]) - 1])
                        
                        if user in exp1_pp1aTracker:
                            exp1_pp1aTracker[user].append(["Moved to Different Problem", str(time)])

            usersLastMove[user] = [div, move, time]

        for user in exp1_pp1aTracker:

            csv_writer.writerow([user, exp1_pp1aTracker[user]])

            
        
stats_by_problem("SI206-ParsonsData.csv", "test.csv", "Parsons")

