import csv
import os
import datetime as dt
import sys


# function to gather the data on Parsons Problems
def parsons_time_worker(inFileName, outFileName):

    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the output file for writing
    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, outFileName), "w")

    # open the input and output files as csv files
    with open(os.path.join(dir, inFileName)) as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # create a dictionary with every parsons problem
        parsons_prob_dict = {
            "check-guess-Parsons": [],
            "get-middle-Parsons": [],
            "alarm-clock-Parsons": [],
            "speeding-Parsons": [],
            "loop_avg_drop_lowest": [],
            "sum-odd-parsons": [],
            "sum13-parsons": [],
            "filter_words-Parsons": [],
            "pPersonClass1": []
        }

        # loop through the data
        for cols in csv_reader:

            # get the event and user
            user = cols[1]
            time = dt.datetime.strptime(cols[2], "%Y-%m-%d %H:%M:%S")
            move = cols[4]
            problemName = cols[5]


            if problemName in parsons_prob_dict:




            # filters Parson Problems
            if event == "parsonsMove" and move.split('|')[0] == "start":

                user_dict[user].append(time)


            elif event == "parsons" and len(user_dict[user]) > 0:

                user_dict[user][len(user_dict[user]) - 1] = time - user_dict[user][len(user_dict[user]) - 1]

                if move.split('|')[0] == "incorrect":

                    user_dict[user].append(time)


        for user in user_dict:

            # writes the data on Parson Problems to the file
            csv_writer.writerow([user, user_dict[user]])


    outFile.close()



parsons_worker("SI206-Win20-Anon.csv", "SI206-ParsonsTimes.csv")
