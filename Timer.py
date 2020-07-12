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
        probUserTimer = dict()
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
                if div not in probUserTimer:
                    probUserTimer[div] = {}
                userDict = probUserTimer[div]

                # track when user starts a problem and add the timestamp to probUserTimer
                if user not in userDict:
                    probUserTimer[div][user] = UserTimer()
                    if move.split('|')[0] == "start" or move == "edit":
                        probUserTimer[div][user].lastDatetime = time

                elif user in userCurrentProblem:

                    # check if user is working on this problem and is on their first attempt
                    if div not in userCompletedProblems[user] and div == userCurrentProblem[user]:

                        # if time between moves is greater than five minutes, remove that time
                        if probUserTimer[div][user].lastDatetime is not None and (time - probUserTimer[div][user].lastDatetime) > dt.timedelta(minutes=5):
                            probUserTimer[div][user].lastDatetime = None
                        elif probUserTimer[div][user].lastDatetime is not None:
                            timedelta = time - probUserTimer[div][user].lastDatetime
                            probUserTimer[div][user].accumulatedTimeSeconds += timedelta.seconds
                        
                        # add completed problems to userCompletedProblems
                        if move.split('|')[0] == "correct" or move.split('.')[0] == "percent:100": 
                            userCompletedProblems[user].append(div)
                            del userCurrentProblem[user]
                        else:
                            probUserTimer[div][user].lastDatetime = time
                    
                    # when user goes to different question, pause time to previous question and begin timer on new question
                    elif div not in userCompletedProblems[user] and div != userCurrentProblem[user]:
                        
                        if userCurrentProblem[user] in probUserTimer:
                            probUserTimer[userCurrentProblem[user]][user].lastDatetime = None
                        probUserTimer[div][user].lastDatetime = time

            userCurrentProblem[user] = div

    return probUserTimer

# function that times how long a user works on a problem their second attempt
def second_attempt_problem_timer(inFileName, eventTypeArray, usersCompletedProb):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the input and output files as csv files
    with open(inFileName) as csv_file:
        csv_reader = csv.reader(csv_file)

        # create an empty timer dictionary and dictionaries that tracks a user's current problem / completed problems
        probUserTimer = dict()
        userCurrentProblem = dict()
        userCompletedSecondAttempt = dict()

        # loop through the data
        for cols in csv_reader:

            # collect data from row
            user = cols[1]
            time = dt.datetime.strptime(cols[2], "%Y-%m-%d %H:%M:%S")
            event = cols[3]
            move = cols[4]
            div = cols[5]

            if event in eventTypeArray and user in usersCompletedProb and div in usersCompletedProb[div]:

                # create array of problems a user has completed
                if user not in userCompletedSecondAttempt:
                    userCompletedSecondAttempt[user]= []

                # if no dictionary for this problem create one and add this user and time
                if div not in probUserTimer:
                    probUserTimer[div] = {}
                userDict = probUserTimer[div]

                # track when user starts a problem and add the timestamp to probUserTimer
                if user not in userDict:
                    probUserTimer[div][user] = UserTimer()
                    if move.split('|')[0] == "start" or move == "edit":
                        probUserTimer[div][user].lastDatetime = time

                elif user in userCurrentProblem:

                    # check if user is working on this problem and is on their first attempt
                    if div not in userCompletedSecondAttempt[user] and div == userCurrentProblem[user]:

                        # if time between moves is greater than five minutes, remove that time
                        if probUserTimer[div][user].lastDatetime is not None and (time - probUserTimer[div][user].lastDatetime) > dt.timedelta(minutes=5):
                            probUserTimer[div][user].lastDatetime = None
                        elif probUserTimer[div][user].lastDatetime is not None:
                            timedelta = time - probUserTimer[div][user].lastDatetime
                            probUserTimer[div][user].accumulatedTimeSeconds += timedelta.seconds
                        
                        # add completed problems to userCompletedProblems
                        if move.split('|')[0] == "correct" or move.split('.')[0] == "percent:100": 
                            userCompletedSecondAttempt[user].append(div)
                            del userCurrentProblem[user]
                        else:
                            probUserTimer[div][user].lastDatetime = time
                    
                    # when user goes to different question, pause time to previous question and begin timer on new question
                    elif div not in userCompletedSecondAttempt[user] and div != userCurrentProblem[user]:
                        
                        if userCurrentProblem[user] in probUserTimer:
                            probUserTimer[userCurrentProblem[user]][user].lastDatetime = None
                        probUserTimer[div][user].lastDatetime = time

            userCurrentProblem[user] = div

    return probUserTimer, userCompletedSecondAttempt