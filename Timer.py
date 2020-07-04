import csv
import os
import sys
import math
import datetime as dt
import numpy as ny

# class that acts as a stopwatch for user
class UserTimer:
    accumulatedTimeSeconds = 0 # time accumulated from working on a problem
    lastDatetime = None # most current datetime a user has worked on a problem
    
# function that times how long a user works on a problem
def problem_timer(inFileName, eventTypeArray):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the input and output files as csv files
    with open(inFileName) as csv_file:
        csv_reader = csv.reader(csv_file)

        # create an empty timer dictionary and dictionaries that tracks a user's current problem / completed problems
        probDict = dict()
        userCurrentProblem = dict()
        userCompletedProblems = dict()

        # loop through the data
        for cols in csv_reader:

            # collect data from row
            user = cols[1]
            time = dt.datetime.strptime(cols[2], "%Y-%m-%d %H:%M:%S")
            event = cols[3]
            move = cols[4]
            div = cols[5]

            if event in eventTypeArray:

                # create array of problems a user has completed
                if user not in userCompletedProblems:
                    userCompletedProblems[user]= []

                # if no dictionary for this problem create one and add this user and time
                if div not in probDict:
                    probDict[div] = {}
                userDict = probDict[div]

                # track when user starts a problem and add the timestamp to probDict
                if user not in userDict:
                    probDict[div][user] = UserTimer()
                    if move.split('|')[0] == "start" or move == "edit":
                        probDict[div][user].lastDatetime = time

                elif user in userCurrentProblem:

                    # check if user is working on this problem and is on their first attempt
                    if div not in userCompletedProblems[user] and div == userCurrentProblem[user]:

                        # if time between moves is greater than five minutes, remove that time
                        if probDict[div][user].lastDatetime is not None and (time - probDict[div][user].lastDatetime) > dt.timedelta(minutes=5):
                            probDict[div][user].lastDatetime = None
                        elif probDict[div][user].lastDatetime is not None:
                            timedelta = time - probDict[div][user].lastDatetime
                            probDict[div][user].accumulatedTimeSeconds += timedelta.seconds
                        
                        # add completed problems to userCompletedProblems
                        if move.split('|')[0] == "correct" or move.split('.')[0] == "percent:100": 
                            userCompletedProblems[user].append(div)
                            del userCurrentProblem[user]
                        else:
                            probDict[div][user].lastDatetime = time
                    
                    # when user goes to different question, pause time to previous question and begin timer on new question
                    elif div not in userCompletedProblems[user] and div != userCurrentProblem[user]:
                        
                        if userCurrentProblem[user] in probDict:
                            probDict[userCurrentProblem[user]][user].lastDatetime = None
                        probDict[div][user].lastDatetime = time

            userCurrentProblem[user] = div

    return probDict


timerDict = problem_timer("SI206-Win20-Anon.csv", ["parsonsMove", "parsons"])

 
