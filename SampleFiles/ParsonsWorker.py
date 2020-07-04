import csv
import os
import datetime as dt
import sys


def correct(answer):
    return (answer.find("correct") >= 0)

    
def addAnswer(userDict, user, timestamp, answer):
    answerDict = {}
    userDict[user] = answerDict
    answerDict["timestamp"] = timestamp
    answerDict["answer"] = answer

def is_earlier(daytime1, daytime2):
    #t1 = dt.datetime.strptime(daytime1, "%m/%d/%y %H:%M")
    #t2 = dt.datetime.strptime(daytime2, "%m/%d/%y %H:%M")
    t1 = dt.datetime.strptime(daytime1, "%Y-%m-%d %H:%M:%S")
    t2 = dt.datetime.strptime(daytime2, "%Y-%m-%d %H:%M:%S")
    latest = max(t1, t2)
    if latest == t1:
        return False
    return True

# function to gather the data on the mchoice questions
def parsons_worker(inFileName, outFileName):
    
    # set the field size to max
    csv.field_size_limit(sys.maxsize)

    # open the output file for writing
    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, outFileName), "w")

    # open the input and output files as csv files
    with open(os.path.join(dir, inFileName)) as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # create an empty book dictionary
        book_dict = dict()

        # loop through the data
        for cols in csv_reader:

            # get the event
            event = cols[2]

            # if mChoice
            if event == "parsons":

                # get the divid, user, timestamp, and answer
                div = cols[4]
                user = cols[1]
                timestamp = cols[0]
                answer = cols[3]
                book = cols[6]

                # if no dictionary for this book add one
                if book not in book_dict:
                    book_dict[book] = dict()
                probDict = book_dict[book]

                # if no dictionary for this problem create one and add this user and answer
                if div not in probDict:
                    userDict = {}
                    probDict[div] = userDict
                else:
                    userDict = probDict[div]

                # if user in dictionary
                if user in userDict:

                    # check if answer is earlier and replace if it is
                    # also replace if the first was undefined
                    answerDict = userDict[user]
                    oldTime = answerDict["timestamp"]
                    curr_answer = answerDict["answer"]
                    if is_earlier(timestamp, oldTime) or curr_answer.find("undefined") >= 0:
                        answerDict["timestamp"] = timestamp
                        answerDict["answer"] = answer
                  
                else:
                    addAnswer(userDict, user, timestamp, answer)

        # now loop through each book
        for book in book_dict:

            # set the totals per book to 0
            count_book = 0
            total_below_20 = 0
            total_20_40 = 0
            total_40_60 = 0
            total_60_80 = 0
            total_above_80 = 0

            # get the problem dictionary
            probDict = book_dict[book]

            # for each multiple choice question total the number of correct first responses
            for prob in probDict:
 
                # increment the number of problems in the book
                count_book += 1
                total_correct = 0
               

                # loop through the users
                user_dict = probDict[prob]
                for user in user_dict:

                    # get the answer and see if correct
                    answerDict = user_dict[user]
                    answer = answerDict["answer"]
                    if correct(answer):
                        total_correct += 1
                    
                # calcuate the total attemped and percent correct
                total_attempted = len(user_dict)
                percent_correct = (total_correct / total_attempted) * 100

                # add the to appropriate total
                if percent_correct < 20:
                    total_below_20 += 1
                elif percent_correct < 40:
                    total_20_40 += 1
                elif percent_correct < 60:
                    total_40_60 += 1
                elif percent_correct < 80:
                    total_60_80 += 1
                else:
                    total_above_80 += 1


                # write the information to the file
                csv_writer.writerow([prob, total_correct, total_attempted, percent_correct, book])

            print(f'total parson problems for book {book} was {count_book}')
            print(f'total below 20% correct {total_below_20} percent {total_below_20 / count_book * 100}')
            print(f'total 20 to 40% correct {total_20_40}  percent {total_20_40 / count_book * 100}')
            print(f'total between 40 and 60% correct {total_40_60} percent {total_40_60 / count_book * 100}')
            print(f'total between 60 and 80% correct {total_60_80} percent {total_60_80 / count_book * 100}')
            print(f'total above 80% correct {total_above_80} percent {total_above_80 / count_book * 100}')


    outFile.close()

parsons_worker("log-12-19.csv", "parsons-log-12-19.csv")
