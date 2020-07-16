import csv
import os
import sys
from StatsWorker import *
from Timer import problem_timer, second_attempt_problem_timer

def problem_1(averageStdDevDict, attemptedCompletedDict, probPercentCompleted, outFileName):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the output file for writing
    dir = os.path.dirname(__file__)

    # open the input and output files as csv files
    with open(os.path.join(dir, outFileName), "w") as outFile:
        csv_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for div in averageStdDevDict:

            if div in attemptedCompletedDict and div in probPercentCompleted:

                csv_writer.writerow([div, averageStdDevDict[div][0], averageStdDevDict[div][1], attemptedCompletedDict[div][0], attemptedCompletedDict[div][1], probPercentCompleted[div]])

    outFile.close()

def carl_exp1_pp1a(timerDict, outFileName):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the output file for writing
    dir = os.path.dirname(__file__)

    # open the input and output files as csv files
    with open(os.path.join(dir, outFileName), "w") as outFile:
        csv_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for div in timerDict:

            if div == "exp1_pp1a":
                for user in timerDict[div]:

                    csv_writer.writerow([user, timerDict[div][user].accumulatedTimeSeconds])

    outFile.close()

def problem_5_part1(attemptedCompletedDict, usersResetProb, outFileName):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the output file for writing
    dir = os.path.dirname(__file__)

    # open the input and output files as csv files
    with open(os.path.join(dir, outFileName), "w") as outFile:
        csv_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        numberUniqueUsersReset = {}

        for div in usersResetProb:
            count = 0
            for user in usersResetProb[div]:
                if usersResetProb[div][user] == True:
                    count += 1
            numberUniqueUsersReset[div] = count

        for div in numberUniqueUsersReset:
            if div in attemptedCompletedDict:

                csv_writer.writerow([div, attemptedCompletedDict[div][0], attemptedCompletedDict[div][1], numberUniqueUsersReset[div]])

    outFile.close()

def problem_5_part2(averageStdDevDictFirstAttempt, averageStdDevDictSecondAttempt, userCompletedSecondAttempt, outFileName):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the output file for writing
    dir = os.path.dirname(__file__)

    # open the input and output files as csv files
    with open(os.path.join(dir, outFileName), "w") as outFile:
        csv_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for div in averageStdDevDictFirstAttempt:
            if div in averageStdDevDictSecondAttempt:
                csv_writer.writerow([div, averageStdDevDictFirstAttempt[div][0], averageStdDevDictSecondAttempt[div][0]])
            else:
                csv_writer.writerow([div, averageStdDevDictFirstAttempt[div][0], "0"])

    outFile.close()



errorStateStatsDict = error_state_collector("SI206-Win20-Anon.csv")


# problem_1(averageStdDevDict, attemptedCompletedDict, probPercentCompleted, "ParsonsTimes.csv")
# problem_1(averageStdDevDict, attemptedCompletedDict, probPercentCompleted, "ActiveCodeTimes.csv")
# carl_exp1_pp1a(timerDictParsons, "exp1_pp1aStats.csv")
# problem_5_part1(probAttemptedCompleted, usersResetProb, "problem5part1.csv")
# problem_5_part2(averageStdDevDictFirstAttempt, averageStdDevDictSecondAttempt, userCompletedSecondAttempt, "problem5part2.csv")

