import csv
import os
import sys
import math
import datetime as dt
import numpy as ny


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
                userDict = {}
                probAttempts[div] = userDict
            else:
                userDict = probAttempts[div]

            # if user is new, set user to 0 attempts
            if user not in userDict:
                probAttempts[div][user] = 0

            if user not in usersCompletedProb:
                usersCompletedProb[user] = []

            if move.split('|')[0] == "correct" and div not in usersCompletedProb[user]:
                probAttempts[div][user] += 1
                usersCompletedProb[user].append(div)

            elif user in userDict and move.split('|')[0] == "incorrect" and div not in usersCompletedProb[user]:
                probAttempts[div][user] += 1

    return probAttempts


def users_attempted_completed_prob(inFileName, probDict):

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

            if user not in usersCompletedProb:
                usersCompletedProb[user] = []

            if move.split('|')[0] == "correct" and div not in usersCompletedProb[user]:
                probAttemptedCompleted[div][1] += 1
                usersCompletedProb[user].append(div)

        for div in probDict:
            usersAttempted = 0
            for user in probDict[div]:
                if probDict[div][user] > 0:
                    usersAttempted += 1
            probAttemptedCompleted[div][0] = usersAttempted

    return probAttemptedCompleted


def prob_percent_completed(probDict):

    probPercentCompleted = dict()

    for div in probDict:
        if probDict[div][0] > 0:
            probPercentCompleted[div] = (probDict[div][1] / probDict[div][0]) * 100
        else:
            probPercentCompleted[div] = 0


probAttempts = users_attempts_prob("SI206-Win20-Anon.csv")
probAttemptedCompleted = users_attempted_completed_prob("SI206-Win20-Anon.csv", probAttempts)
prob_percent_completed(probAttemptedCompleted)