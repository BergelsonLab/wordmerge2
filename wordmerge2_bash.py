import sys
import os
import csv
import wordmerge2 as wm2
import datetime

def runWordmerge2(old_folder, new_folder):
	newFileList = []
	oldFileList = []
	delta = 0
	mark = True
	fixCount = 0
	caseCount = 0
	timeCount = 0
	for file in os.listdir(old_folder):
		file = os.path.join(old_folder, file)
		if file.endswith("sparse_code.csv"):
			oldFileList.append(file)
		elif file.endswith("processed.csv"):
			newFileList.append(file)
	for oldFile in oldFileList:
		for newFile in newFileList:
			oldDate = getdates(oldFile)
			newDate = getdates(newFile)
			if oldDate == newDate:
				fix, case, time = wm2.merge(oldFile, newFile, new_folder, delta, mark)
				fixCount += fix
				caseCount += case
				timeCount += time
	writeLog(new_folder, fixCount, caseCount, timeCount)


#get prefix from full path file
def getdates(file):
	pathList = re.split("\\\|/", file) #file.split("/")
	fileName = pathList[-1]
	dateList = re.split("\\\|/", fileName) #fileName.split("_")
	date = dateList[0] + "_" + dateList[1]
	return date

#print out log file
def writeLog(new_folder, fixCount, caseCount, timeCount):
	countRow = [fixCount, caseCount, timeCount]
	pathList = re.split("\\\|/", new_folder) #new_folder.split("/")
	now = datetime.datetime.now()
	currentD = datetime.date(now.year, now.month, now.day)
	fileName = currentD.isoformat() + "_count_log.csv"
	fullName = ""
	for i in range(len(pathList)):
		fullName += pathList[i]
		fullName += "/"
	fullName += fileName
	with open(fullName, "wb") as writefile:
		writer = csv.writer(writefile)
		writer.writerow(countRow)

if __name__ == "__main__":
	

	old_folder = sys.argv[1]
	new_folder = sys.argv[2]

	runWordmerge2(old_folder, new_folder)
