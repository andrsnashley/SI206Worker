import csv
import os
import datetime as dt
import sys


def correct(answer):
    return (answer.find("correct") >= 0)

def getAnswerNum(answer):
    posFirstCol = answer.find(":")
    posSecondCol = answer.find(":", posFirstCol + 1)
    item = answer[posFirstCol + 1: posSecondCol]
    return item
    
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
def mchoice_worker(inFileName, outFileName):
    
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
            if event == "mChoice":

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
                total_a = 0
                total_b = 0
                total_c = 0
                total_d = 0
                total_e = 0
                total_undef = 0

                # loop through the users
                user_dict = probDict[prob]
                for user in user_dict:

                    # get the answer and see if correct
                    answerDict = user_dict[user]
                    answer = answerDict["answer"]
                    item = getAnswerNum(answer)
                    if correct(answer):
                        total_correct += 1
                    if item == "0":
                        total_a += 1
                    elif item == "1":
                        total_b += 1
                    elif item == "2":
                        total_c += 1
                    elif item == "3":
                        total_d += 1
                    elif item == "4":
                        total_e += 1
                    else: 
                        total_undef += 1

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

                per_a = total_a / total_attempted * 100
                per_b = total_b / total_attempted * 100
                per_c = total_c / total_attempted * 100
                per_d = total_d / total_attempted * 100
                per_e = total_d / total_attempted * 100
                per_undef = total_undef / total_attempted * 100

                # write the information to the file
                csv_writer.writerow([prob, total_correct, total_attempted, percent_correct, total_a, per_a, 
                  total_b, per_b, total_c, per_c, total_d, per_d, total_e, per_e, total_undef, per_undef, book])

            print(f'total mc problems for book {book} was {count_book}')
            print(f'total below 20% correct {total_below_20} percent {total_below_20 / count_book * 100}')
            print(f'total 20 to 40% correct {total_20_40}  percent {total_20_40 / count_book * 100}')
            print(f'total between 40 and 60% correct {total_40_60} percent {total_40_60 / count_book * 100}')
            print(f'total between 60 and 80% correct {total_60_80} percent {total_60_80 / count_book * 100}')
            print(f'total above 80% correct {total_above_80} percent {total_above_80 / count_book * 100}')


    outFile.close()

mchoice_worker("log-12-19.csv", "mChoice-log-12-19.csv")
