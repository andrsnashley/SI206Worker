import csv
import os
import sys
import math
import datetime as dt
import numpy as ny

def users_attempted_completed_prob(inFileName, outFileName):

        # set the field size to max
        csv.field_size_limit(sys.maxsize)

        # open the output file for writing
        dir = os.path.dirname(__file__)
        outFile = open(os.path.join(dir, outFileName), "w")

        # open the input and output files as csv files
        with open(os.path.join(dir, inFileName)) as csv_file:
            csv_reader = csv.reader(csv_file)
            csv_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # create dictionary that tracks a users completion status of problems
            probDict = dict()
            usersCompletedProb = dict()

            # loop through the data
            for cols in csv_reader:

                # get the user, move, and problem name
                user = cols[1]
                move = cols[4]
                div = cols[5]

                # if no dictionary for this problem create one and add this user
                if div not in probDict:
                    userDict = {}
                    probDict[div] = userDict
                else:
                    userDict = probDict[div]

                if user not in userDict:
                    probDict[div][user] = []

                if user not in usersCompletedProb:

                    usersCompletedProb[user] = []

                if user in userDict and move.split('|')[0] == "correct" and div not in usersCompletedProb[user]:

                    probDict[div][user] += 1

                    usersCompletedProb[user].append(div)

                elif user in userDict and move.split('|')[0] == "incorrect" and div not in usersCompletedProb[user]:

                    probDict[div][user] += 1

            csv_writer.writerow(["Problem Div", "Attempted", "Correct", "25%", "50%", "75%", "100%"])

            # output the stats for each problem type
            for div in probDict:

                usersAttempted = 0
                usersCorrect = 0
                numAttemptsArray = []

                for user in probDict[div]:

                    if probDict[div][user] != 0:

                        if user in usersCompletedProb and div in usersCompletedProb[user]:

                            usersCorrect += 1
                            numAttemptsArray.append(probDict[div][user])

                        usersAttempted += 1