# importing csv module 
import csv, string, os, math
import operator

# Globals
allTeamAnswers = []
answerKey = []
answerPoints = []
outputTextFileName = ""
outputCsvFileName = ""
roundName = ""
outputFolderName = ""
perAnswerInfo = []
perTeamInfo = []

def main():
    initializeOutputVariables()
    ReadCsvs()
    numGraders = input("How many graders?: ")
    teamsPerGrader = len(allTeamAnswers) / int(numGraders)
    CreateResultsFolder()
    scores = {}
    i = 1
    for teamAnswers in allTeamAnswers:
        print("Processing Answers for Team: " + teamAnswers[1])
        scores[teamAnswers[1]] = CheckAnswers(teamAnswers[1], teamAnswers[2:len(teamAnswers)])
        if i % int(teamsPerGrader) == 0:
            UpdateOutputFileNames(math.ceil(i / teamsPerGrader))
            writePerAnswerInfoToTextFile()
            writePerTeamInfoToCsv()
            initializeOutputVariables()

        i += 1
    print("For convenience, results are located in the " + outputFolderName + " folder.")
    print("Program has Finished!")

def UpdateOutputFileNames(graderId):
    global outputTextFileName
    global outputCsvFileName

    outputTextFileName = "DetailedResults_" + str(graderId) +".txt"
    outputCsvFileName = "Results_" + str(graderId) + ".csv"

def ReadCsvs():
    global answerKey
    global answerPoints
    global allTeamAnswers
    global roundName
    print("\nBelow are the files in this folder:\n")
    os.system('ls')
    print("\n")
    answerKeyFile = input("Answer Key File Name: ")
    teamAnswerFiles = input("Round Answers File Name: ")
    roundName = teamAnswerFiles.split(".")[0]
    # answerKeyFile = "Round 1_AnswerKey.csv"
    # teamAnswerFiles = "Round 1.csv"
    answerFields = []
    answerKeyFields = []
    with open(answerKeyFile, 'r') as csvfile: 
        answerKeyReader = csv.reader(csvfile)
        answerKeyFields = next(answerKeyReader) 
        answerKey = next(answerKeyReader)
        answerPoints = next(answerKeyReader)

    with open(teamAnswerFiles, 'r') as csvfile: 
        teamAnswersReader = csv.reader(csvfile)
        answerFields = next(teamAnswersReader)
        sortedlist = sorted(teamAnswersReader, key=lambda row: row[1].lower(), reverse=False)
        for row in sortedlist: 
            allTeamAnswers.append(row)

def CompareCleansedAnswers(teamAnswer, officialAnswer):
    correct = 0
    for teamAnswerPart in teamAnswer:
        if teamAnswerPart in officialAnswer:
            correct += 1
            officialAnswer.remove(teamAnswerPart)
    return correct


def CheckAnswers(teamName, teamAnswers):
    global perAnswerInfo
    global perTeamInfo

    answerInfoInsertLocation = len(perAnswerInfo)
    score = 0
    for i in range(0, len(answerKey)):
        cleansedTeamAnswer = []
        cleansedOfficialAnswer = []
        # Get single answer as a list
        if "&" in teamAnswers[i]:
            teamAnswer = teamAnswers[i].split("&")
        else:
            teamAnswer = teamAnswers[i].split(",")
        for teamAnswerPart in teamAnswer:
            # Cleanse all parts of answer of all white space
            cleansedTeamAnswer.append(cleanWord(teamAnswerPart))
        officialAnswer = answerKey[i].split(",")
        for officialAnswerPart in officialAnswer:
            cleansedOfficialAnswer.append(cleanWord(officialAnswerPart))
        answerScore = CompareCleansedAnswers(cleansedTeamAnswer, cleansedOfficialAnswer)
        score += answerScore
        if answerPoints[i] != str(answerScore):
            perAnswerInfo.append("%s\t%s\t%s\t%s\t|\t%s" % ("Question_" + str(i + 1), answerPoints[i], str(answerScore), teamAnswers[i], answerKey[i]))
    perAnswerInfo.insert(answerInfoInsertLocation, "\n%s --> %s" % (teamName, str(score)))
    perTeamInfo.append([teamName, str(score)])
    return score

# Removes punctuation, gets rid of whitespace, converts to lower case
def cleanWord(word):
    cleansedWord = word
    cleansedWord = cleansedWord.translate(str.maketrans('','',string.punctuation))
    cleansedWord = "".join(cleansedWord.split())
    cleansedWord = cleansedWord.lower()
    return cleansedWord

def writePerAnswerInfoToTextFile():
    global perAnswerInfo
    info = ""
    for line in perAnswerInfo:
        info = info + line + "\n"
    outputFile = open(os.path.join(outputFolderName, outputTextFileName), "w")
    outputFile.write(info)
    outputFile.close()

def writePerTeamInfoToCsv():
    global perTeamInfo
    with open(os.path.join(outputFolderName, outputCsvFileName), mode='w') as result_file:
        result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in perTeamInfo:
            result_writer.writerow(row)

def CreateResultsFolder():
    global outputFolderName
    currentWorkingDirectory = os.getcwd()
    outputFolderName = roundName + "_Results/"
    resultsPath = os.path.join(currentWorkingDirectory, outputFolderName)
    if os.path.exists(resultsPath) == False:
        os.makedirs(resultsPath)

def initializeOutputVariables():
    global perAnswerInfo
    global perTeamInfo
    perAnswerInfo = ["---\nTeam_Name --> Overall_Score\nQuestion_X, Exp_Score, Act_Score, Team_Ans | Official_Ans\n---"]
    perTeamInfo = [["Team Name","Total Score"]]

if __name__ == "__main__":
    main()


