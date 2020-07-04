import csv
import os
import sys
import math
import datetime as dt
import numpy as ny

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
                    userDict = {}
                    probDict[div] = userDict
                else:
                    userDict = probDict[div]

                # track when user starts a problem and add the timestamp to probDict
                if user not in userDict:
                    probDict[div][user] = []
                    if move.split('|')[0] == "start" or move == "edit":
                        probDict[div][user].append(time)
                        userCurrentProblem[user] = div

                elif user in userCurrentProblem:

                    # check if user is working on this problem and is on their first attempt
                    if div not in userCompletedProblems[user] and div == userCurrentProblem[user]:

                        # if time between moves is greater than five minutes, remove that time
                        if (time - probDict[div][user][len(probDict[div][user]) - 1]) > dt.timedelta(minutes=5):
                            probDict[div][user].pop()
                        else:
                            probDict[div][user][len(probDict[div][user]) - 1] = str(time - probDict[div][user][len(probDict[div][user]) - 1])
                        
                        # add completed problems to userCompletedProblems
                        if move.split('|')[0] == "correct" or move.split('.')[0] == "percent:100": 
                            userCompletedProblems[user].append(div)
                            del userCurrentProblem[user]
                        else:
                            probDict[div][user].append(time)
                            userCurrentProblem[user] = div
                    
                    # when user goes to different question, pause time to previous question and begin timer on new question
                    elif div not in userCompletedProblems[user] and div != userCurrentProblem[user]:
                        
                        if userCurrentProblem[user] in probDict:
                            probDict[userCurrentProblem[user]][user].pop()
                        probDict[div][user].append(time)
                        userCurrentProblem[user] = div

            # check if user is performing a different interaction to pause the time
            elif user in userCurrentProblem:
                if userCurrentProblem[user] in probDict:
                    probDict[userCurrentProblem[user]][user].pop()
                userCurrentProblem[user] = div

        for div in probDict:
            for user in probDict[div]:

                totalTimeToSolve = 0

                for x in range(len(probDict[div][user])):

                    time = probDict[div][user][x]
                    if not isinstance(time, str):
                        totalTimeToSolve += 0
                    else:
                        hh, mm , ss = map(int, time.split(':'))
                        totalTimeToSolve += (ss + 60*(mm + 60*hh))
                
                probDict[div][user] = totalTimeToSolve
                
            csv_writer.writerow([div, probDict[div]])

    outFile.close()



problem_timer("SI206-Win20-Anon.csv", "timerTotalTime.csv", ["parsonsMove", "parsons"])

 
