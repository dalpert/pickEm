# importing csv module 
import csv, string, os, math
import operator, flask
import zipfile

class autoGraderClass:
    def __init__(self, pathToOutputDirectory):
        self.answerKey = []
        self.answerPoints = []
        self.outputFolder = os.path.join(pathToOutputDirectory, "output")
        self.rawOutputFileName = "_rawAnswers.csv"
        self.detailedOutputFileName = "_details.txt"
        self.answerKeyFileName = "_answerKey.csv"
        self.teamScoresOutputCsvName = "_scores.csv"
        self.perAnswerInfo = []
        self.perTeamInfo = []
        self.roundId = ""
    
    def gradeAndWriteFiles(self, allTeamAnswers, fullAnswerKey, roundId):
        self.initializeOutputFileHeaders()
        self.parseAnswerKey(fullAnswerKey)
        self.roundId = roundId
        scores = {}
        for teamAnswers in allTeamAnswers:
            scores[teamAnswers[0]] = self.CheckAnswers(teamAnswers[0], teamAnswers[1:len(teamAnswers)])
        
        self.writeDetailedInfoToTextFile()
        self.writeTeamScoresToCsvFile()
        self.writeRawDataToTextFile(allTeamAnswers)
        self.writeAnswerKeyToTextFile(fullAnswerKey, roundId)

    def parseAnswerKey(self, answerKey):
        self.answerKey = answerKey[0]
        self.answerPoints = answerKey[1]

    def CompareCleansedAnswers(self, teamAnswer, officialAnswer):
        correct = 0
        for teamAnswerPart in teamAnswer:
            if teamAnswerPart in officialAnswer:
                correct += 1
                officialAnswer.remove(teamAnswerPart)
        return correct
    
    def CheckAnswers(self, teamName, teamAnswers):
        answerInfoInsertLocation = len(self.perAnswerInfo)
        score = 0
        for i in range(0, len(teamAnswers)):
            cleansedTeamAnswer = []
            cleansedOfficialAnswer = []
            # Get single answer as a list
            if "&" in teamAnswers[i]:
                teamAnswer = teamAnswers[i].split("&")
            else:
                teamAnswer = teamAnswers[i].split(",")

            for teamAnswerPart in teamAnswer:
                # Cleanse all parts of answer of all white space
                cleansedTeamAnswer.append(self.cleanWord(teamAnswerPart))
            officialAnswer = self.answerKey[i].split(",")
            for officialAnswerPart in officialAnswer:
                cleansedOfficialAnswer.append(self.cleanWord(officialAnswerPart))
            answerScore = self.CompareCleansedAnswers(cleansedTeamAnswer, cleansedOfficialAnswer)
            score += answerScore
            if self.answerPoints[i] != str(answerScore):
                self.perAnswerInfo.append("%s\t%s\t%s\t%s\t|\t%s" % ("Question_" + str(i + 1), self.answerPoints[i], str(answerScore), teamAnswers[i] if len(teamAnswers[i]) > 0 else "[No Answer]", self.answerKey[i]))
        self.perAnswerInfo.insert(answerInfoInsertLocation, "\n%s --> %s" % (teamName, str(score)))
        self.perTeamInfo.append([teamName, str(score)])
        return score
    
    # Removes punctuation, gets rid of whitespace, converts to lower case
    def cleanWord(self, word):
        cleansedWord = word
        cleansedWord = cleansedWord.translate(str.maketrans('','',string.punctuation))
        cleansedWord = "".join(cleansedWord.split())
        cleansedWord = cleansedWord.lower()
        return cleansedWord
    
    def writeDetailedInfoToTextFile(self):
        self.perAnswerInfo
        info = ""
        for line in self.perAnswerInfo:
            info = info + line + "\n"
        outputFile = open(os.path.join(self.outputFolder, self.roundId + self.detailedOutputFileName), "w")
        outputFile.write(info)
        outputFile.close()

    def writeRawDataToTextFile(self, rawData):
        rawData.insert(0, ["Team Name", "Question 1", "Question 2", "Question 3", "Question 4", "Question 5", "Question 6"])
        with open(os.path.join(self.outputFolder, self.roundId + self.rawOutputFileName), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rawData)

    def writeAnswerKeyToTextFile(self, answerKey, roundId):
        answerKey.insert(0, ["Question Numbers", "Question 1", "Question 2", "Question 3", "Question 4", "Question 5", "Question 6"])
        answerKey[1].insert(0, "Correct Answer")
        answerKey[2].insert(0, "Max Score")
        with open(os.path.join(self.outputFolder, roundId + self.answerKeyFileName), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(answerKey)
    
    def writeTeamScoresToCsvFile(self):
        self.perTeamInfo
        with open(os.path.join(self.outputFolder, self.roundId + self.teamScoresOutputCsvName), mode='w') as result_file:
            result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in self.perTeamInfo:
                result_writer.writerow(row)
    
    def initializeOutputFileHeaders(self):
        self.perAnswerInfo = ["---\nTeam_Name --> Overall_Score\nQuestion_X, Exp_Score, Act_Score, Team_Ans | Official_Ans\n---"]
        self.perTeamInfo = [["Team Name","Total Score"]]


