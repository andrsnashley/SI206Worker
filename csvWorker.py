import csv
import os
import sys
from StatsWorker import *
from Timer import problem_timer

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


timerDictParsons = problem_timer("SI206-Win20-Anon.csv", ["parsonsMove", "parsons"])
timerDictActiveCode = problem_timer("SI206-Win20-Anon.csv", ["activecode", "unittest", "ac_error"])
probAttempts = users_attempts_prob("SI206-Win20-Anon.csv")
usersCompletedProb = users_completed("SI206-Win20-Anon.csv")
attemptedCompletedDict = prob_attempted_completed_prob("SI206-Win20-Anon.csv", probAttempts)
probPercentCompleted = prob_percent_completed(attemptedCompletedDict)
averageStdDevDict = prob_timer_average_stdDev(timerDictActiveCode, usersCompletedProb)

# problem_1(averageStdDevDict, attemptedCompletedDict, probPercentCompleted, "testing.csv")
problem_1(averageStdDevDict, attemptedCompletedDict, probPercentCompleted, "testingActiveCode.csv")
# carl_exp1_pp1a(timerDictParsons, "exp1_pp1aStats.csv")