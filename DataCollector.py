import csv
import os
import datetime as dt
import numpy as ny
import sys
import math

parsonsEventNames = ["parsonsMove", "parsons"]

activecodeEventNames = ["activecode", "unittest", "ac_error"]

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

        # create dictionary that tracks a users completion status of problems
        usersCompletedProb = dict()
        usersAttemptedProb = dict()

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

            if user not in usersCompletedProb:

                usersCompletedProb[user] = []

            if user not in usersAttemptedProb:

                usersAttemptedProb[user] = []

            # track when user starts a problem and add the timestamp to probDict
            if user not in userDict:

                probDict[div][user] = []
                probDict[div][user].append(time)

            # only edits the timestamp if user in already in probDict and the user has started the problem
            if user in userDict and div not in usersCompletedProb[user]:

                # track the time user is spending on a problem
                if not isinstance(probDict[div][user][len(probDict[div][user]) - 1], str):

                    if time - probDict[div][user][len(probDict[div][user]) - 1] > dt.timedelta(minutes=5):

                        probDict[div][user].pop(len(probDict[div][user]) - 1)
                        probDict[div][user].append(time)

                    elif move == "differentProblem":

                        probDict[div][user][len(probDict[div][user]) - 1] = str(time - probDict[div][user][len(probDict[div][user]) - 1])

                    # when student gets problem correct, ends the time tracking and adds user to usersCompletedProb
                    if move.split('|')[0] == "correct" or move.split('.')[0] == "percent:100":

                        probDict[div][user][len(probDict[div][user]) - 1] = str(time - probDict[div][user][len(probDict[div][user]) - 1])

                        usersCompletedProb[user].append(div)
                        usersAttemptedProb[user].append(div)

                        for x in range(len(probDict[div][user])):

                            if not isinstance(probDict[div][user][x], str):

                                probDict[div][user].pop(x)

                    elif move.split('|')[0] == "incorrect" or move.split(':')[0] == "percent":

                        usersAttemptedProb[user].append(div)

                elif isinstance(probDict[div][user][len(probDict[div][user]) - 1], str):

                    if move != "differentProblem":

                        probDict[div][user].append(time)

        for div in probDict:

            if div == "alarm-clock-Parsons" or div == "alarm_clock":

                for user in probDict[div]:

                    csv_writer.writerow([user, probDict[div][user]])

    outFile.close()

    #     csv_writer.writerow(["Problem Div", "Problem Type", "Average", "StdDev", "Attempted", "Correct", "Percent Correct"])

    #     # output the stats for each problem type
    #     for div in probDict:
        
    #         csv_writer.writerow([div, probDict[div]])

    #         usersAttempted = 0
    #         usersCorrect = 0
    #         totalTime = 0
    #         stdDevX = []
            
    #         for user in probDict[div]:
            
    #             if div in usersAttemptedProb[user]:
            
    #                 if div in usersCompletedProb[user]:
            
    #                     usersCorrect += 1
    #                     timeforUser = 0
            
    #                     for time in probDict[div][user]:
            
    #                         try:
            
    #                             hh, mm , ss = map(int, time.split(':'))
    #                             totalTime += (ss + 60*(mm + 60*hh))
    #                             timeforUser += (ss + 60*(mm + 60*hh))
            
    #                         except:
            
    #                             totalTime += 0
            
    #                     stdDevX.append(timeforUser)
            
    #                 usersAttempted += 1
            
    #         if usersAttempted == 0:
            
    #                 probDict[div].pop('differentProblem', None)
            
    #         else:
            
    #             if usersCorrect == 0:
            
    #                 usersAverage = 0
    #                 usersStdDev = 0
            
    #             else:
            
    #                 usersAverage = totalTime / usersCorrect
    #                 usersStdDev = 0
            
    #                 for x in stdDevX:
            
    #                      attempt = x - usersAverage
    #                      usersStdDev += pow(attempt, 2)
            
    #                 try:
            
    #                     usersStdDev = math.sqrt(usersStdDev / (usersCorrect - 1))
            
    #                 except:
            
    #                     usersStdDev = math.sqrt(usersStdDev / usersCorrect)
            
    #             percentCorrect = usersCorrect / usersAttempted
            
    #             csv_writer.writerow([div, problemType, usersAverage, usersStdDev, usersAttempted, usersCorrect, percentCorrect])

    # outFile.close()

# function that creates a CSV file with quartile statistics for each problem
def quartile_by_problem(inFileName, outFileName):

        # set the field size to max
        csv.field_size_limit(sys.maxsize)

        # open the output file for writing
        dir = os.path.dirname(__file__)
        outFile = open(os.path.join(dir, outFileName), "w")

        # open the input and output files as csv files
        with open(os.path.join(dir, inFileName)) as csv_file:
            csv_reader = csv.reader(csv_file)
            csv_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # create dictionary that tracks the quartiles per problem
            probDict = dict()

            # create dictionary that tracks a users completion status of problems
            usersCompletedProb = dict()

            # loop through the data
            for cols in csv_reader:

                # get the user, time, move, and problem name
                user = cols[1]
                move = cols[4]
                div = cols[5]

                if cols[3] == "parsons" or cols[3] == "parsonsMove":

                    # if no dictionary for this problem create one and add this user
                    if div not in probDict:

                        userDict = {}
                        probDict[div] = userDict

                    else:

                        userDict = probDict[div]

                    if user not in userDict:

                        probDict[div][user] = 0

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

                if usersCorrect == 0:

                    firstQuartile = 0
                    median = 0
                    thirdQuartile = 0
                    max = 0

                else:

                    print(numAttemptsArray)
                    firstQuartile = math.ceil(ny.percentile(numAttemptsArray, 25))
                    median = math.ceil(ny.percentile(numAttemptsArray, 50))
                    thirdQuartile = math.ceil(ny.percentile(numAttemptsArray, 75))
                    max = math.ceil(ny.percentile(numAttemptsArray, 100))

                csv_writer.writerow([div, usersAttempted, usersCorrect, firstQuartile, median, thirdQuartile, max])

        outFile.close()

# function that creates a CSV file with the statistics on Parson Adaptions
def parson_adaptation_stats(inFileName, outFileName):

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

        usersUsedAdaptation = dict()
        usersAdaptation = dict()
        usersUniqueAdaptation = dict()
        usersAbusedAdaptation = dict()

        # loop through the data
        for cols in csv_reader:

            # get the user, time, move, and problem name
            user = cols[0]
            move = cols[2]
            div = cols[3]

            # if no dictionary for this problem create one and add this user and answer
            if div not in probDict:

                probDict[div] = [0, 0, 0, 0, 0]

            if div not in usersAdaptation:

                usersAdaptation[div] = {}

            if user not in usersAdaptation[div]:

                usersAdaptation[div][user] = False

            if div not in usersUniqueAdaptation:

                usersUniqueAdaptation[div] = {}

            if user not in usersUniqueAdaptation[div]:

                usersUniqueAdaptation[div][user] = [False, False, False]

            if div not in usersUsedAdaptation:

                usersUsedAdaptation[div] = {}

            if div not in usersAbusedAdaptation:

                usersAbusedAdaptation[div] = {}

            if user not in usersAbusedAdaptation[div]:

                usersAbusedAdaptation[div][user] = [-1, 0]

            if move.split('-')[0] == "removedDistractor":

                probDict[div][0] += 1
                usersAdaptation[div][user] = True
                usersUsedAdaptation[div][user] = True
                usersUniqueAdaptation[div][user][0] = True
                if usersAbusedAdaptation[div][user][0] == -1:
                    usersAbusedAdaptation[div][user][0] = 0
                elif usersAbusedAdaptation[div][user][0] == 0:
                    usersAbusedAdaptation[div][user][1] += 1
                elif usersAbusedAdaptation[div][user][0] > 0:
                    usersAbusedAdaptation[div][user][0] = 100

            elif move.split('|')[0] == "removedIndentation":

                probDict[div][1] += 1
                usersAdaptation[div][user] = True
                usersUsedAdaptation[div][user] = True
                usersUniqueAdaptation[div][user][1] = True
                if usersAbusedAdaptation[div][user][0] == -1:
                    usersAbusedAdaptation[div][user][0] = 0
                elif usersAbusedAdaptation[div][user][0] == 0:
                    usersAbusedAdaptation[div][user][1] += 1
                elif usersAbusedAdaptation[div][user][0] > 0:
                    usersAbusedAdaptation[div][user][0] = 100

            elif move.split('|')[0] == "combinedBlocks":

                probDict[div][2] += 1
                usersAdaptation[div][user] = True
                usersUsedAdaptation[div][user] = True
                usersUniqueAdaptation[div][user][2] = True
                if usersAbusedAdaptation[div][user][0] == -1:
                    usersAbusedAdaptation[div][user][0] = 0
                elif usersAbusedAdaptation[div][user][0] == 0:
                    usersAbusedAdaptation[div][user][1] += 1
                elif usersAbusedAdaptation[div][user][0] > 0:
                    usersAbusedAdaptation[div][user][0] = 100
                    
            elif move.split('|')[0] == "move" and usersAdaptation[div][user] == True:

                probDict[div][3] += 1
                usersAdaptation[div][user] = False
                if usersAbusedAdaptation[div][user][0] == 0:
                    usersAbusedAdaptation[div][user][0] += 1

            elif move.split('|')[0] == "correct":

                if usersAbusedAdaptation[div][user][0] < 3 and usersAbusedAdaptation[div][user][0] >= 0:
                    usersAbusedAdaptation[div][user][0] = -5

            else:

                usersAdaptation[div][user] = False

        

        # output the stats for each problem type
        for div in probDict:

            sum = 0
            numberAbusedAdaptation = 0

            for user in usersUsedAdaptation[div]:
                if usersUsedAdaptation[div][user] == True:
                    sum += 1

            for user in usersAbusedAdaptation[div]:
                if usersAbusedAdaptation[div][user][0] == -5 and usersAbusedAdaptation[div][user][1] > 1:
                    numberAbusedAdaptation += 1

            csv_writer.writerow([div, sum, numberAbusedAdaptation])

        # Code for unique users per adaptation

        # for div in usersUniqueAdaptation:
        #
        #     count = 0
        #     for user in usersUniqueAdaptation[div]:
        #         if usersUniqueAdaptation[div][user][2] == True:
        #
        #             count += 1
        #     csv_writer.writerow([count])


    outFile.close()

# function to fitler the data on a type of Problem
def problem_filter(inFileName, outFileName, eventNameArray):

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
        user_problem_completion_dict = dict()

        # loop through the data
        for cols in csv_reader:

            # get the event and user
            user = cols[1]
            move = cols[4]
            event = cols[3]

            # writes each log for the type of problem to CSV file
            if event in eventNameArray:

                # writes the data on the problem to the file
                csv_writer.writerow([user, cols[2], cols[4], cols[5]])

                # sets if user solved the problem
                if move.split('|')[0] == "correct" or move.split('.')[0] == "percent:100":

                    user_problem_completion_dict[user] = "Complete"

                else:

                    user_problem_completion_dict[user] = "Incomplete"

            # writes out a line if the user moved to a different problem
            if event not in eventNameArray and user in user_problem_completion_dict:

                if user_problem_completion_dict[user] == "Incomplete":

                    csv_writer.writerow([user, cols[2], "differentProblem", "differentProblem"])



    outFile.close()



