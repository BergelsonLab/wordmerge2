import sys
import os
import csv
import re
import wordmerge2 as wm2
import datetime

def runWordmerge2(old_folder, new_folder):
	newFileList = []
	oldFileList = []
	fileCount = []
	fileError = []
	delta = 0
	mark = True
	printLog = False
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
				fix, case, time, isAudio, newFileName, old_error, new_error = wm2.merge(oldFile, newFile, new_folder, delta, mark, printLog)
				fileCount.append([getFileName(newFileName), fix, case, time])
				fixCount += fix
				caseCount += case
				timeCount += time
				fileError.append(sortError(getFileName(oldFile), old_error, isAudio))
				fileError.append(sortError(getFileName(newFile), new_error, isAudio))
	writeCountLog(new_folder, fixCount, caseCount, timeCount, fileCount)
	writeErrorLog(new_folder, fileError, isAudio)
	printFix(fixCount, caseCount, timeCount)


#get prefix from full path file
def getdates(file):
	pathList = re.split("\\\|/", file) #file.split("/")
	fileName = pathList[-1]
	dateList = fileName.split("_")
	date = dateList[0] + "_" + dateList[1]
	return date

def printFix(fixCount, caseCount, timeCount):
	asterisk = "********************************************************************"
	nl = "\n"
	alert = nl + nl + asterisk + nl + asterisk + nl + nl
	fixMsg = "TOTAL:" + nl + repr(fixCount) + " ***FIX ME***, " + repr(caseCount) + " *CASE*, " + repr(timeCount) + " *TIME* "

	print alert + fixMsg + alert

def getFileName(path):
	pathList = re.split("\\\|/", path)
	fileName = pathList[-1]
	return fileName

def sortError(file, errorlist, isAudio):
	if isAudio:
		return sortAudioError(file, errorlist)
	else:
		return sortVideoError(file, errorlist)

def sortAudioError(file, errorlist):
	tier = 0
	word = 0
	utter = 0
	o_p = 0
	speaker = 0
	timestamp = 0
	basic = 0
	for error in errorlist:
		if error[2] == "tier":
			tier += 1
		elif error[2] == "word":
			word += 1
		elif error[2] == "utterance_type":
			utter += 1
		elif error[2] == "object_present":
			o_p += 1
		elif error[2] == "speaker":
			speaker += 1
		elif error[2] == "timestamp":
			timestamp += 1
		elif error[2] == "basic_level":
			basic += 1
	return [file, repr(tier), repr(word), repr(utter), repr(o_p), repr(speaker), repr(timestamp), repr(basic)]

def sortVideoError(file, errorlist):
	ordinal = 0
	obj = 0
	utter = 0
	o_p = 0
	speaker = 0
	onset = 0
	offset = 0
	basic = 0
	for error in errorlist:
		if error[2] == "labeled_object.ordinal":
			ordinal += 1
		elif error[2] == "labeled_object.object":
			obj += 1
		elif error[2] == "labeled_object.utterance_type":
			utter += 1
		elif error[2] == "labeled_object.object_present":
			o_p += 1
		elif error[2] == "labeled_object.speaker":
			speaker += 1
		elif error[2] == "labeled_object.onset":
			onset += 1
		elif error[2] == "labeled_object.offset":
			offset += 1
		elif error[2] == "labeled_object.basic_level":
			basic += 1
	return [file, repr(ordinal), repr(onset), repr(offset), repr(obj), repr(utter), repr(o_p), repr(speaker), repr(basic)]




#print out log file
def writeCountLog(new_folder, fixCount, caseCount, timeCount, fileCount):
	countRow = ["Total", fixCount, caseCount, timeCount]
	fullName = getFullName(new_folder, "_count_log.csv")
	with open(fullName, "wb") as writefile:
		writer = csv.writer(writefile)
		writer.writerow(["file", "FIX", "CASE", "TIME"])
		for count in fileCount:
			writer.writerow(count)
		writer.writerow(countRow)

def writeErrorLog(new_folder, fileError, isAudio):
	fullName = getFullName(new_folder, "_error_log.csv")
	if isAudio:
		colName = ["file", "tier", "word", "utterance_type", "object_present", "speaker", "timestamp", "basic_level"]
	else:
		colName = ["file", "labeled_object.ordinal", "labeled_object.onset", "labeled_object.offset", "labeled_object.object", "labeled_object.utterance_type", "labeled_object.object_present", "labeled_object.speaker", "labeled_object.basic_level"]
	with open(fullName, "wb") as writefile:
		writer = csv.writer(writefile)
		writer.writerow(colName)
		for error in fileError:
			writer.writerow(error)

def getFullName(new_folder, suffix):
	pathList = re.split("\\\|/", new_folder) #new_folder.split("/")
	now = datetime.datetime.now()
	currentD = datetime.date(now.year, now.month, now.day)
	fileName = currentD.isoformat() + suffix
	fullName = "/"
	for i in range(len(pathList)):
		if not pathList[i]:
			continue
		fullName += pathList[i]
		fullName += "/"
	fullName += fileName
	return fullName


if __name__ == "__main__":
	

	old_folder = sys.argv[1]
	new_folder = sys.argv[2]

	runWordmerge2(old_folder, new_folder)
