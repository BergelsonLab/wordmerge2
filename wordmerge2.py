import sys
import csv
import pandas as pd
import checker
import re
import os

#merge function rewrites the new_file with basic_level column 
#from old_file and returns dataframe of new_file
#parameters: old file path, new file path, error range allowed for timestemp, 
def merge(old_file, new_file, new_file_writeTo, delta, mark, printLog):
    print "\n" + "merging {} --and-- {} .....".format(old_file, new_file) + "\n"
    #clean csv file
    clean(new_file)
    clean(old_file)

    df_old = pd.read_csv(old_file, header = 0, keep_default_na=False)
    df_new = pd.read_csv(new_file, header = 0, keep_default_na=False)

    common_file = "common_words_index.csv"
    commonList = commonNA(common_file)

    if "word" in list(df_old):
    	#Checking for errors for audio file
		new_error = checker.give_error_report_audio(new_file)
		old_error = checker.give_error_report_audio(old_file)
		#cleanBL might be extra, haven't tested yet
		df_old = cleanBL(df_old, "basic_level")
		df_new = cleanBL(df_new, "basic_level")
		df_new, fixCount, caseCount, timeCount = getBasicAudio(df_old, df_new, mark, delta, commonList)
		isAudio = True
    else:
    	#Checking for errors for video file
		new_error = checker.give_error_report_video(new_file)
		old_error = checker.give_error_report_video(old_file)
		#cleanBL might be extra, haven't tested yet
		df_old = cleanBL(df_old, "labeled_object.basic_level")
		df_new = cleanBL(df_new, "labeled_object.basic_level")
		df_new, fixCount, caseCount, timeCount = getBasicVideo(df_old, df_new, mark, delta, commonList)
		isAudio = False

    logPath = newErrorPath(new_file, new_file_writeTo, "log.csv", isAudio)

    #Individual wordmerge run would print log to terminal by default, bash would turn this off
    if printLog:
    	printError(old_error, new_error, logPath)
    	printFix(fixCount, caseCount, timeCount)

    writeErrorLog(old_error, new_error, logPath, getFileName(old_file), getFileName(new_file))
    newFileName = newpath(new_file, new_file_writeTo, "wordmerged.csv", isAudio)
    df_new.to_csv(newFileName, index = False)

    return fixCount, caseCount, timeCount, isAudio, newFileName, old_error, new_error

#print count for fixme, case, time to terminal 
def printFix(fixCount, caseCount, timeCount):
	asterisk = "********************************************************************"
	nl = "\n"
	alert = nl + nl + asterisk + nl + asterisk + nl + nl
	fixMsg = repr(fixCount) + " ***FIX ME***, " + repr(caseCount) + " *CASE*, " + repr(timeCount) + " *TIME* "

	print fixMsg + alert

#print errors to terminal 
def printError(old_error, new_error, logPath):
	asterisk = "********************************************************************"
	nl = "\n"
	alert = nl + asterisk + nl + asterisk + nl
	new_errorCount = len(new_error)
	old_errorCount = len(old_error)

	old_errorMsg = nl + repr(old_errorCount) + " error(s) are detected in the old file:" + nl + nl
	for error in old_error:
		errorMsg = error[2] + " in row " + error[1] + " with word \"" + error[0] + "\""
		old_errorMsg = old_errorMsg + errorMsg + nl
	new_errorMsg = nl + repr(new_errorCount) + " error(s) are detected in the new file:" + nl + nl
	for error in new_error:
		errorMsg = error[2] + " in row " + error[1] + " with word \"" + error[0] + "\""
		new_errorMsg = new_errorMsg + errorMsg + nl
	logMsg = nl + "All errors recorded in " + logPath + nl

	print alert + old_errorMsg + new_errorMsg + logMsg + alert

#genearet csv file for error log
def writeErrorLog(old_error, new_error, logPath, old_fileName, new_fileName):
	with open(logPath, 'w') as writefile:
		writer = csv.writer(writefile)
		writer.writerow(["file", "word", "row", "column_name"]) #need to keep an eye on the row number
		for error in old_error:
			writer.writerow([old_fileName] + error)
		for error in new_error:
			writer.writerow([new_fileName] + error)

#get NA list
def commonNA(common_file):
	df_common = pd.read_csv(common_file, header = 0, usecols = [0, 1, 2, 3], keep_default_na = False)
	commonWord = df_common.loc[df_common["Basic Level"] == "NA", "word"]
	commonWord = [word.lower().replace(" ", "") for word in commonWord]
	return commonWord

#clean basic_level column
def cleanBL(df, colname):
	colArr = df.columns.values
	for i in range(len(colArr)):
		if colArr[i] in ["basic_level", "labeled_object.basic_level"]:
			colArr[i] = colname
	df.columns = colArr
	df[colname] = df[colname].astype(str)
	return df 

#get error log path inside error folder
def newErrorPath(new_file, new_file_writeTo, suffix, isAudio):
	newpathList = re.split("\\\|/", new_file_writeTo)
	newpathList.append("error")
	pathName = combinePath(newpathList)
	if not os.path.exists(pathName):
		os.makedirs(pathName)
	preffix = getPreffix(new_file, suffix, isAudio)
	pathName += preffix
	return pathName

#get single file name from path
def getFileName(path):
	pathList = re.split("\\\|/", path)
	fileName = pathList[-1]
	return fileName

#get new_file_writeTo path
def newpath(new_file, new_file_writeTo, suffix, isAudio):
	preffix = getPreffix(new_file, suffix, isAudio)
	newpathList = re.split("\\\|/", new_file_writeTo)
	fullName = combinePath(newpathList)
	fullName += preffix
	return fullName

#get unique preffix for each pair of files
def getPreffix(new_file, suffix, isAudio):
	fileName = getFileName(new_file)
	prefList = fileName.split("_")
	pref = prefList[0] + "_" + prefList[1] + "_"
	if isAudio:
		pref += "audio" + "_"
	else:
		pref += "video" + "_"
	pref += suffix
	return pref

#combine path list into single path string
def combinePath(pathList):
	fullName = "/"
	for i in range(len(pathList)):
		if ".csv" in pathList[i] or not pathList[i]:
			continue
		fullName += pathList[i]
		fullName += "/"
	return fullName


#clean csv file for pandas reading
def clean(file):
	rowlist = list()
	with open(file, 'rU') as readfile:
		reader = csv.reader(readfile)
		rowlist = [l for l in reader]
		for row in rowlist:
			if row[-1] == "":
				del row[-1]
		if "basic_level" not in rowlist[0]:
			if "labeled_object.basic_level" not in rowlist[0]:
				if "word" in rowlist[0]:
					rowlist[0].append('basic_level')
				else:
					rowlist[0].append("labeled_object.basic_level")
	with open(file, 'wb') as writefile:
		writer = csv.writer(writefile)
		for n in rowlist:
			writer.writerow(n)

#create lowercase version of old_file for video
def lowerDFVideo(df_old):
	df_old_lower = df_old.copy();
	for oldr in range(0, len(df_old_lower.index)):
		objectN = df_old_lower.get_value(oldr, "labeled_object.object")
		df_old_lower.set_value(oldr, "labeled_object.object", objectN.lower().replace(" ", ""))
	return df_old_lower

#create lowercase version of old_file for audio
def lowerDFAudio(df_old):
	df_old_lower = df_old.copy();
	for oldr in range(0, len(df_old_lower.index)):
		objectN = df_old_lower.get_value(oldr, "word")
		df_old_lower.set_value(oldr, "word", objectN.lower().replace(" ", ""))
	return df_old_lower

#return the basic level entry with option to mark or not
def getBasicVideo(df_old, df_new, mark, delta, commonList):
	caseCount = 0
	fixCount = 0
	timeCount = 0
	#get lower case in object column
	for newr in df_new.index:
		df_old_lower = lowerDFVideo(df_old)
		try:
			#assume case if fixed, see if there is a match
			temp_df = df_old_lower.loc[df_old_lower["labeled_object.object"] == df_new.get_value(newr, "labeled_object.object").lower(), ["labeled_object.offset", "labeled_object.onset", "labeled_object.basic_level"]]
			for oldr in temp_df.index:
				addMark = ""
				#for those with case issue, add a mark for case
 				if df_old.get_value(oldr, "labeled_object.object") != df_new.get_value(newr, "labeled_object.object"):
 					addMark = "*CASE*"
				if mark:
	 				addMark = df_old_lower.get_value(oldr, "labeled_object.basic_level") + addMark
	 				df_old_lower.set_value(oldr, "labeled_object.basic_level", addMark)
	 				temp_df.set_value(oldr, "labeled_object.basic_level", addMark)
			temp_df = temp_df.loc[temp_df["labeled_object.offset"] == df_new.get_value(newr, "labeled_object.offset"), ["labeled_object.basic_level", "labeled_object.onset"]]
			blValue = temp_df.loc[temp_df["labeled_object.onset"] == df_new.get_value(newr, "labeled_object.onset"), "labeled_object.basic_level"].values[0]
		except:
			#code break might be caused by unmatch in object or time, case mark already added for any match term with case change
			blValue = getTimeChangeVideo(df_old_lower, newr, df_new, mark, delta)
		if "*CASE*" in blValue:
			caseCount += 1
		if "*TIME*" in blValue:
			timeCount += 1
		if blValue == "***FIX ME***":
			#check if in the common word list
			if df_new.get_value(newr, "labeled_object.object").lower().replace(" ", "") in commonList:
				blValue = "NA"
			else:
				fixCount += 1
		df_new.set_value(newr, "labeled_object.basic_level", blValue)
	return df_new, fixCount, caseCount, timeCount

#check if the timestamp is within the range
def getTimeChangeVideo(df_old_lower, newr, df_new, mark, delta):
	temp_df = df_old_lower.loc[df_old_lower["labeled_object.object"] == df_new.get_value(newr, "labeled_object.object").lower().replace(" ", ""), ["labeled_object.offset", "labeled_object.onset", "labeled_object.basic_level"]]
	#only proceed when there is a match for object column regardless of case
	if not temp_df.empty:
		blValue = "***FIX ME***"
		#for all term that matches for object column but not onset and offset column, try given tolerance to time
		for oldr in temp_df.index:
			oldOnset = temp_df.get_value(oldr, "labeled_object.onset")
			oldOffset = temp_df.get_value(oldr, "labeled_object.offset")
			newOnset = df_new.get_value(newr, "labeled_object.onset")
			newOffset = df_new.get_value(newr, "labeled_object.offset")
			if abs(oldOnset - newOnset) <= delta and abs(oldOffset - newOffset) <= delta:
				#overwrite fix me when there is a time match given the tolerance
				blValue = temp_df.get_value(oldr, "labeled_object.basic_level")
				if mark:
					#might cause overlapping of different basic_level values with a large time tolerance
					blValue = blValue + "*TIME*"
			else:
				continue
	#when no match for object column even change case
	else:
		blValue = "***FIX ME***"
	return blValue

#return the basic level entry with option to mark or not
def getBasicAudio(df_old, df_new, mark, delta, commonList):
	caseCount = 0
	fixCount = 0
	timeCount = 0
	for newr in df_new.index:
		#get lower case in word column
		df_old_lower = lowerDFAudio(df_old)
		try:
			#assume case if fixed, see if there is a match
			temp_df = df_old_lower.loc[df_old_lower["tier"] == df_new.get_value(newr, "tier"), ["word", "timestamp", "basic_level"]]
 			temp_df = temp_df.loc[temp_df["word"] == df_new.get_value(newr, "word").lower().replace(" ", ""), ["basic_level", "timestamp", "word"]]
 			for oldr in temp_df.index:
 				addMark = ""
 				#for those with case issue, add a mark for case
 				if df_old.get_value(oldr, "word") != df_new.get_value(newr, "word"):
 					addMark = "*CASE*"
 				if mark:
	 				addMark = df_old_lower.get_value(oldr, "basic_level") + addMark
	 				df_old_lower.set_value(oldr, "basic_level", addMark)
	 				temp_df.set_value(oldr, "basic_level", addMark)
 			blValue = temp_df.loc[temp_df["timestamp"] == df_new.get_value(newr, "timestamp"), "basic_level"].values[0]
		except:
			#code break might be caused by unmatch in word, tier and time, case mark already added for any match term with case change
			blValue = getTimeChangeAudio(df_old_lower, df_new, newr, mark, delta)
		if "*CASE*" in blValue:
			caseCount += 1
		if "*TIME*" in blValue:
			timeCount += 1
		if blValue == "***FIX ME***":
			#check if in the common word list
			if df_new.get_value(newr, "word").lower().replace(" ", "") in commonList:
				blValue = "NA"
			else:
				fixCount += 1
		df_new.set_value(newr, "basic_level", blValue)	
	return df_new, fixCount, caseCount, timeCount


#check if the timestamp is within the range
def getTimeChangeAudio(df_old_lower, df_new, newr, mark, delta):
	temp_df = df_old_lower.loc[df_old_lower["tier"] == df_new.get_value(newr, "tier"), ["word", "timestamp", "basic_level"]]
	temp_df = temp_df.loc[temp_df["word"] == df_new.get_value(newr, "word").lower().replace(" ", ""), ["basic_level", "timestamp"]]
	#only proceed when there is a match for word column regardless of case and tier column
	if not temp_df.empty:
		blValue = "***FIX ME***"
		#for all term that matches for word and tier column but not timestamp column, try given tolerance to time
		for oldr in temp_df.index:
			oldTimestamp = temp_df.get_value(oldr, "timestamp").split("_")
			newTimestamp = df_new.get_value(newr, "timestamp").split("_")
			oldOnset = int(oldTimestamp[0])
			oldOffset = int(oldTimestamp[1])
			newOnset = int(newTimestamp[0])
			newOffset = int(newTimestamp[1])
			if abs(oldOnset - newOnset) <= delta and abs(oldOffset - newOffset) <= delta:
				#overwrite fix me when there is a time match given the tolerance
				blValue = temp_df.get_value(oldr, "basic_level")
				if mark:
					#might cause overlapping of different basic_level values with a large time tolerance
					blValue = blValue + "*TIME*"
			else:
				continue
	#when no match for object column or tier column even change case
	else:
		blValue = "***FIX ME***"
	return blValue



if __name__ == "__main__":
	#default value for last three inputs
	delta = 0
	mark = True
	printLog = True

	#new error list every run
	new_error = []
	old_error = []

	#input argument from terminal 
	old_file = sys.argv[1]
	new_file = sys.argv[2]
	new_file_writeTo = sys.argv[3]
	if len(sys.argv) >= 5:
		delta = int(sys.argv[4])
	if len(sys.argv) >= 6:
		mark = sys.argv[5].lower().replace(" ", "") == "true"
	if len(sys.argv) >= 7:
		printLog = sys.argv[5].lower().replace(" ", "") == "true"

	#call main merge function
	merge(old_file, new_file, new_file_writeTo, delta, mark, printLog)
