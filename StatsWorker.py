import csv
import os
import sys
import math
import datetime as dt
import numpy as ny
from collections import OrderedDict
from statistics import mean, stdev 


def users_attempts_prob(inFileName):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the input and output files as csv files
    with open(inFileName) as csv_file:
        csv_reader = csv.reader(csv_file)

        # create an empty attempts dictionary and one that tracks a users completion status of problems
        probAttempts = dict()
        usersCompletedProb = dict()

        # loop through the data
        for cols in csv_reader:

            # get the user, move, and problem name
            user = cols[1]
            move = cols[4]
            div = cols[5]

            # if no dictionary for this problem create one and add this user
            if div not in probAttempts:
                probAttempts[div] = {}
            userDict = probAttempts[div]

            # if user is new, set user to 0 attempts
            if user not in userDict:
                probAttempts[div][user] = 0

            if user not in usersCompletedProb:
                usersCompletedProb[user] = []

            if (move.split('|')[0] == "correct" or move.split('.')[0] == "percent:100") and div not in usersCompletedProb[user]:
                probAttempts[div][user] += 1
                usersCompletedProb[user].append(div)

            elif user in userDict and (move.split('|')[0] == "incorrect" or move.split(':')[0] == "percent") and div not in usersCompletedProb[user]:
                probAttempts[div][user] += 1

    return probAttempts

def prob_attempted_completed_prob(inFileName, probAttempts):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the input and output files as csv files
    with open(inFileName) as csv_file:
        csv_reader = csv.reader(csv_file)

        # create an empty attempts dictionary and one that tracks a users completion status of problems
        probAttemptedCompleted = dict()
        usersCompletedProb = dict()

        # loop through the data
        for cols in csv_reader:

            # get the user, move, and problem name
            user = cols[1]
            move = cols[4]
            div = cols[5]

            # if no dictionary for this problem create one and add this user
            if div not in probAttemptedCompleted:
                probAttemptedCompleted[div] = [0, 0] # number of users who attempted and completed
                usersAttempted = 0
                for user in probAttempts[div]:
                    if probAttempts[div][user] > 0:
                        usersAttempted += 1
                probAttemptedCompleted[div][0] = usersAttempted


            if user not in usersCompletedProb:
                usersCompletedProb[user] = []

            if (move.split('|')[0] == "correct" or move.split('.')[0] == "percent:100") and div not in usersCompletedProb[user]:
                probAttemptedCompleted[div][1] += 1
                usersCompletedProb[user].append(div)

    return probAttemptedCompleted

def prob_percent_completed(attemptedCompletedDict):

    probPercentCompleted = dict()

    for div in attemptedCompletedDict:
        if attemptedCompletedDict[div][0] > 0:
            probPercentCompleted[div] = (attemptedCompletedDict[div][1] / attemptedCompletedDict[div][0]) * 100
        else:
            probPercentCompleted[div] = 0
        
    return probPercentCompleted

def users_completed(inFileName):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the input and output files as csv files
    with open(inFileName) as csv_file:
        csv_reader = csv.reader(csv_file)

        # create an empty  dictionary that tracks a users completion status of problems
        usersCompletedProb = dict()

        # loop through the data
        for cols in csv_reader:

            # get the user, move, and problem name
            user = cols[1]
            move = cols[4]
            div = cols[5]

            if user not in usersCompletedProb:
                usersCompletedProb[user] = []

            if (move.split('|')[0] == "correct" or move.split('.')[0] == "percent:100") and div not in usersCompletedProb[user]:
                usersCompletedProb[user].append(div)

    return usersCompletedProb

def prob_timer_average_stdDev(timerDict, usersCompletedProb):

    probAverageStdDev = dict()

    # output the stats for each problem type
    for div in timerDict:

        timeList = []
        
        for user in timerDict[div]:
        
            if user in usersCompletedProb and div in usersCompletedProb[user]:

                timeList.append(timerDict[div][user].accumulatedTimeSeconds)
        
        if len(timeList) > 1:
            average = mean(timeList)
            stdDev = stdev(timeList)
        elif len(timeList) > 0:
            average = mean(timeList)
            stdDev = 0
        else:
            average = 0
            stdDev = 0

        probAverageStdDev[div] = [average, stdDev]
    
    return probAverageStdDev
            
def users_who_reset(inFileName, usersCompletedProb):

     # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the input and output files as csv files
    with open(inFileName) as csv_file:
        csv_reader = csv.reader(csv_file)

        # create an empty  dictionary that tracks a users completion status of problems
        usersResetProb = dict()
        usersLastMove = dict()

        # loop through the data
        for cols in csv_reader:

            # get the user, move, and problem name
            user = cols[1]
            event = cols[3]
            move = cols[4]
            div = cols[5]

            if event == "parsons" or event == "parsonsMove":

                if div not in usersResetProb:
                    usersResetProb[div] = {}
                if user not in usersResetProb[div]:
                    usersResetProb[div][user] = False

                if move.split('|')[0] == "reset":
                    if user in usersCompletedProb and div in usersCompletedProb[user] and usersLastMove[user][1] == div and usersLastMove[user][0].split('|')[0] == "correct":
                        usersResetProb[div][user] = True
                
            usersLastMove[user] = [move, div]
            
    return usersResetProb

def error_state_collector(inFileName):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the input and output files as csv files
    with open(inFileName) as csv_file:
        csv_reader = csv.reader(csv_file)

        # create an empty  dictionary that tracks a users completion status of problems
        probTotalErrorStates = dict()

        # loop through the data
        for cols in csv_reader:

            # get the user, move, and problem name
            event = cols[3]
            move = cols[4]
            div = cols[5]

            if event == "parsons" or event == "parsonsMove":

                if move.split('|')[0] == "incorrect":

                    if div not in probTotalErrorStates:
                        probTotalErrorStates[div] = {}

                    errorState = move.split('|')[1] + "|" + move.split('|')[2]
                    if errorState in probTotalErrorStates[div]:
                        probTotalErrorStates[div][errorState] += 1
                    else:
                        probTotalErrorStates[div][errorState] = 1

        for div in probTotalErrorStates:

            orderedErrorStates = OrderedDict(sorted(probTotalErrorStates[div].items(), key=lambda x: x[1]))

    return probTotalErrorStates

