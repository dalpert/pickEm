# importing csv module 
import csv, string, os, math
import operator

class autoGraderClass:
    def __init__(self):
        self.answerKey = []
        self.answerPoints = []
        self.rawOutputFileName = "/results/raw.txt"
        self.detailedOutputFileName = "/results/details.txt"
        self.teamScoresOutputCsvName = "/results/scores.csv"
        self.perAnswerInfo = []
        self.perTeamInfo = []
    
    def run(self, allTeamAnswers, fullAnswerKey):
        initializeOutputFileHeaders()
        writeRawDataToTestFile(fullAnswerKey)
        parseAnswerKey(fullAnswerKey)
        scores = {}
        for teamAnswers in allTeamAnswers:
            scores[teamAnswers[1]] = CheckAnswers(teamAnswers[1], teamAnswers[2:len(teamAnswers)])
        
        writeDetailedInfoToTextFile()
        writeTeamScoresToCsvFile()

    def parseAnswerKey(self, answerKey):
        self.answerKey = answerKey[1]
        self.answerPoints = answerKey[2]

    def CompareCleansedAnswers(self, teamAnswer, officialAnswer):
        correct = 0
        for teamAnswerPart in teamAnswer:
            if teamAnswerPart in officialAnswer:
                correct += 1
                officialAnswer.remove(teamAnswerPart)
        return correct
    
    
    def CheckAnswers(self, teamName, teamAnswers):
        self.perAnswerInfo
        self.perTeamInfo
    
        answerInfoInsertLocation = len(self.perAnswerInfo)
        score = 0
        for i in range(0, len(self.answerKey)):
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
            officialAnswer = self.answerKey[i].split(",")
            for officialAnswerPart in officialAnswer:
                cleansedOfficialAnswer.append(cleanWord(officialAnswerPart))
            answerScore = CompareCleansedAnswers(cleansedTeamAnswer, cleansedOfficialAnswer)
            score += answerScore
            if self.answerPoints[i] != str(answerScore):
                self.perAnswerInfo.append("%s\t%s\t%s\t%s\t|\t%s" % ("Question_" + str(i + 1), self.answerPoints[i], str(answerScore), teamAnswers[i], self.answerKey[i]))
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
        outputFile = open(self.detailedOutputFileName, "w")
        outputFile.write(info)
        outputFile.close()

    def writeRawDataToTestFile(self, rawData):
        with open(self.rawOutputFileName, mode='w') as result_file:
            result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in rawData:
                result_writer.writerow(row)
    
    def writeTeamScoresToCsvFile(self):
        self.perTeamInfo
        with open(self.teamScoresOutputCsvName, mode='w') as result_file:
            result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in self.perTeamInfo:
                result_writer.writerow(row)
    
    def initializeOutputFileHeaders(self):
        self.perAnswerInfo = ["---\nTeam_Name --> Overall_Score\nQuestion_X, Exp_Score, Act_Score, Team_Ans | Official_Ans\n---"]
        self.perTeamInfo = [["Team Name","Total Score"]]


