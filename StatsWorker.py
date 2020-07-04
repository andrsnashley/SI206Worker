import csv
import os
import sys
import math
import datetime as dt
import numpy as ny

class UserProblemState:
    accumulatedTimeSeconds = 0
    lastDatetime = None
    
# 
def problem_timer(inFileName, outFileName, eventTypeArray):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the output file for writing
    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, outFileName), "w")

    # open the input and output files as csv files
    with open(os.path.join(dir, inFileName)) as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # create an empty timer dictionary and dictionaries that tracks a user's current problem / completed problems
        probUserState = dict()
        userCurrentProblem = dict()
        userCompletedProblems = dict()

        # loop through the data
        for cols in csv_reader:

            # collect data from row
            user = cols[1]
            time = dt.datetime.strptime(cols[2], "%Y-%m-%d %H:%M:%S")
            event = cols[3]
            move = cols[4]
            rowProblem = cols[5]

            if event in eventTypeArray:

                # create array of problems a user has completed
                if user not in userCompletedProblems:
                    userCompletedProblems[user]= []

                # if no dictionary for this problem create one and add this user and time
                if rowProblem not in probUserState:
                    probUserState[rowProblem] = {}
                userDict = probUserState[rowProblem]

                # track when user starts a problem and add the timestamp to probUserState
                if user not in userDict:
                    probUserState[rowProblem][user] = UserProblemState()
                    if move.split('|')[0] == "start" or move == "edit":
                        probUserState[rowProblem][user].lastDatetime = time

                elif user in userCurrentProblem:

                    # check if user is working on this problem and is on their first attempt
                    if rowProblem not in userCompletedProblems[user] and rowProblem == userCurrentProblem[user]:

                        # if time between moves is greater than five minutes, remove that time
                        if probUserState[rowProblem][user].lastDatetime is not None and (time - probUserState[rowProblem][user].lastDatetime) > dt.timedelta(minutes=5):
                            probUserState[rowProblem][user].lastDatetime = None
                        elif probUserState[rowProblem][user].lastDatetime is not None:
                            timedelta = time - probUserState[rowProblem][user].lastDatetime
                            probUserState[rowProblem][user].accumulatedTimeSeconds += timedelta.seconds
                        
                        # add completed problems to userCompletedProblems
                        if move.split('|')[0] == "correct" or move.split('.')[0] == "percent:100": 
                            userCompletedProblems[user].append(rowProblem)
                            del userCurrentProblem[user]
                        else:
                            probUserState[rowProblem][user].lastDatetime = time
                    
                    # when user goes to different question, pause time to previous question and begin timer on new question
                    elif rowProblem not in userCompletedProblems[user] and rowProblem != userCurrentProblem[user]:
                        
                        if userCurrentProblem[user] in probUserState:
                            probUserState[userCurrentProblem[user]][user].lastDatetime = None
                        probUserState[rowProblem][user].lastDatetime = time

            userCurrentProblem[user] = rowProblem

        for rowProblem in probUserState:
            for user in probUserState[rowProblem]:
 
                csv_writer.writerow([rowProblem, user, probUserState[rowProblem][user].accumulatedTimeSeconds])

    outFile.close()



problem_timer("SI206-Win20-Anon.csv", "timerClassAttempt.csv", ["parsonsMove", "parsons"])

 
