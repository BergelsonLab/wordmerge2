import sys
import csv
import pandas as pd
import codecheck
import re
import os

comment = "%com:"
error_log = []

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
		#cleanBL might be extra, haven't tested yet
		df_old = cleanBL(df_old, "basic_level")
		df_new = cleanBL(df_new, "basic_level")
		df_new, fixCount, caseCount, timeCount = getBasicAudio(df_old, df_new, mark, delta, commonList)
		isAudio = True
    else:
		#cleanBL might be extra, haven't tested yet
		df_old = cleanBL(df_old, "labeled_object.basic_level")
		df_new = cleanBL(df_new, "labeled_object.basic_level")
		df_new, fixCount, caseCount, timeCount = getBasicVideo(df_old, df_new, mark, delta, commonList)
		isAudio = False

	#generate wordmerged csv file
    newFileName = newpath(new_file, new_file_writeTo, "wordmerged.csv", isAudio)
    df_new.to_csv(newFileName, index = False)

    errorList = give_error_report(newFileName)

    logPath = newErrorPath(new_file, new_file_writeTo, "log.csv", isAudio)

    #Individual wordmerge run would print log to terminal by default, bash would turn this off
    if printLog:
    	printError(errorList, logPath)
    	printFix(fixCount, caseCount, timeCount)

    writeErrorLog(errorList, logPath, newFileName)

    return fixCount, caseCount, timeCount, isAudio, newFileName, errorList

#print count for fixme, case, time to terminal 
def printFix(fixCount, caseCount, timeCount):
	asterisk = "********************************************************************"
	nl = "\n"
	alert = nl + nl + asterisk + nl + asterisk + nl + nl
	fixMsg = repr(fixCount) + " ***FIX ME***, " + repr(caseCount) + " *CASE*, " + repr(timeCount) + " *TIME* "

	print fixMsg + alert

#print errors to terminal 
def printError(errorList, logPath):
	asterisk = "********************************************************************"
	nl = "\n"
	alert = nl + asterisk + nl + asterisk + nl
	errorCount = len(errorList)

	errorMsgP = nl + repr(errorCount) + " error(s) are detected in the wordmerged file:" + nl + nl
	for error in errorList:
		errorMsg = error[2] + " in row " + error[1] + " with word \"" + error[0] + "\""
		errorMsgP = errorMsgP + errorMsg + nl
	logMsg = nl + "All errors recorded in " + logPath + nl

	print alert + errorMsgP + logMsg + alert

#genearet csv file for error log
def writeErrorLog(errorList, logPath, newpath):
	newFileName = os.path.basename(newpath)
	with open(logPath, 'w') as writefile:
		writer = csv.writer(writefile)
		writer.writerow(["file", "word", "row", "column_name"]) #need to keep an eye on the row number
		for error in errorList:
			writer.writerow([newFileName] + error)

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
	newpathList = os.path.split(new_file_writeTo)
	if newpathList[1]:
		pathName = os.path.join(newpathList[0], newpathList[1], "error")
	else:
		pathName = os.path.join(newpathList[0], "error")
	if not os.path.exists(pathName):
		os.makedirs(pathName)
	preffix = getPreffix(new_file, suffix, isAudio)
	pathName = os.path.join(pathName, preffix)
	return pathName


#get new_file_writeTo path
def newpath(new_file, new_file_writeTo, suffix, isAudio):
	preffix = getPreffix(new_file, suffix, isAudio)
	newpathList = os.path.split(new_file_writeTo)
	if newpathList[1]:
		pathName = os.path.join(newpathList[0], newpathList[1], preffix)
	else:
		pathName = os.path.join(newpathList[0], preffix)
	return pathName

#get unique preffix for each pair of files
def getPreffix(new_file, suffix, isAudio):
	fileName = os.path.basename(new_file)
	prefList = fileName.split("_")
	pref = prefList[0] + "_" + prefList[1] + "_"
	if isAudio:
		pref += "audio" + "_"
	else:
		pref += "video" + "_"
	pref += suffix
	return pref


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
		df_old_lower.set_value(oldr, "labeled_object.object", objectN.lower())
	return df_old_lower

#create lowercase version of old_file for audio
def lowerDFAudio(df_old):
	df_old_lower = df_old.copy();
	for oldr in range(0, len(df_old_lower.index)):
		objectN = df_old_lower.get_value(oldr, "word")
		df_old_lower.set_value(oldr, "word", objectN.lower())
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
			if df_new.get_value(newr, "labeled_object.object").lower() in commonList or df_new.get_value(newr, "labeled_object.object").startswith(comment):
				blValue = "NA" 
			else:
				fixCount += 1
		df_new.set_value(newr, "labeled_object.basic_level", blValue)
	return df_new, fixCount, caseCount, timeCount

#check if the timestamp is within the range
def getTimeChangeVideo(df_old_lower, newr, df_new, mark, delta):
	temp_df = df_old_lower.loc[df_old_lower["labeled_object.object"] == df_new.get_value(newr, "labeled_object.object").lower(), ["labeled_object.offset", "labeled_object.onset", "labeled_object.basic_level"]]
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
 			temp_df = temp_df.loc[temp_df["word"] == df_new.get_value(newr, "word").lower(), ["basic_level", "timestamp", "word"]]
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
			if df_new.get_value(newr, "word").lower() in commonList or df_new.get_value(newr, "word").startswith(comment):
				blValue = "NA"
			else:
				fixCount += 1
		df_new.set_value(newr, "basic_level", blValue)	
	return df_new, fixCount, caseCount, timeCount


#check if the timestamp is within the range
def getTimeChangeAudio(df_old_lower, df_new, newr, mark, delta):
	temp_df = df_old_lower.loc[df_old_lower["tier"] == df_new.get_value(newr, "tier"), ["word", "timestamp", "basic_level"]]
	temp_df = temp_df.loc[temp_df["word"] == df_new.get_value(newr, "word").lower(), ["basic_level", "timestamp"]]
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

#get error log for video file
def give_error_report_video(info):
    global error_log
    error_log = []
    global ordinal_list
    ordinal_list = []
    video_info = info


    #get index for each column
    colName = video_info[0]
    for i in range(len(colName)):
        if colName[i] == "labeled_object.ordinal":
            ordinalI = i
        elif colName[i] == "labeled_object.onset":
            onsetI = i
        elif colName[i] == "labeled_object.offset":
            offsetI = i
        elif colName[i] == "labeled_object.utterance_type":
            utterI = i
        elif colName[i] == "labeled_object.object":
            objI = i
        elif colName[i] == "labeled_object.object_present":
            obj_preI = i
        elif colName[i] == "labeled_object.speaker":
            speakerI = i
        elif colName[i] == "labeled_object.basic_level" or colName[i] == "basic_level":
            basicI = i

    #check each column from each row
    total_lines = len(video_info)
    line_number = 1
    for row in video_info:
        if not line_number == 1:

            if not codecheck.check_ordinal_video(row[ordinalI], total_lines, ordinal_list):
                error_log.append([row[objI], str(line_number), "labeled_object.ordinal"])
            ordinal_list.append(row[ordinalI])

            if not codecheck.check_onset_video(row[onsetI]):
                error_log.append([row[objI], str(line_number), "labeled_object.onset"])

            if not codecheck.check_offset_video(row[offsetI]):
                error_log.append([row[objI], str(line_number), "labeled_object.offset"])

            if not codecheck.check_object_video(row[objI]):
                error_log.append([row[objI], str(line_number), "labeled_object.object"])

            if not codecheck.check_utterance_type_video(row[utterI], row[objI]):
                error_log.append([row[objI], str(line_number), "labeled_object.utterance_type"])

            if not codecheck.check_object_present_video(row[obj_preI], row[objI]):
                error_log.append([row[objI], str(line_number), "labeled_object.object_present"])

            if not codecheck.check_speaker_video(row[speakerI], row[objI]):
                error_log.append([row[objI], str(line_number), "labeled_object.speaker"])

            #check basic level when there is one
            if len(row) > 7:
                if not codecheck.check_basic_level_video(row[basicI], row[objI]):
                    error_log.append([row[objI], str(line_number), "labeled_object.basic_level"])

        line_number += 1
    return error_log


#get error log for video file
def give_error_report_audio(info):
    global error_log
    error_log = []
    audio_info = info


    #get index for each column
    colName = audio_info[0]
    for i in range(len(colName)):
        if colName[i] == "tier":
            tierI = i
        elif colName[i] == "word":
            wordI = i
        elif colName[i] == "utterance_type":
            utterI = i
        elif colName[i] == "object_present":
            obj_preI = i
        elif colName[i] == "speaker":
            speakerI = i
        elif colName[i] == "timestamp":
            timestampI = i
        elif colName[i] == "basic_level":
            basicI = i

    #check each column from each row
    line_number = 1
    for row in audio_info: 
        if not line_number == 1:
            if not codecheck.check_tier_audio(row[tierI]):
                error_log.append([row[wordI], str(line_number), "tier"])
            
            if not codecheck.check_word_audio(row[wordI]):
                error_log.append([row[wordI], str(line_number), "word"])
            
            if not codecheck.check_utterance_type_audio(row[utterI]):
                error_log.append([row[wordI], str(line_number), "utterance_type"])

            if not codecheck.check_object_present_audio(row[obj_preI]):
                error_log.append([row[wordI], str(line_number), "object_present"])

            if not codecheck.check_speaker_audio(row[speakerI]):
                error_log.append([row[wordI], str(line_number), "speaker"])
            
            if not codecheck.check_timestamp_audio(row[timestampI]):
                error_log.append([row[wordI], str(line_number), "timestamp"])

            #check basic level when there is one
            if len(row) > 6:
            	if not codecheck.check_basic_level_audio(row[basicI]):
                	error_log.append([row[wordI], str(line_number), "basic_level"])

        line_number += 1
    return error_log

# read in csv file and call the right function based on the file type
def give_error_report(filepath):
    info = []
    with open(filepath, 'rt') as csvfileR:
        reader = csv.reader(csvfileR)
        for row in reader:
            info.append(row)

    if "word" in info[0]:
        error_log = give_error_report_audio(info)
    else:
        error_log = give_error_report_video(info)

    return error_log
    


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
		mark = sys.argv[5].lower() == "true"
	if len(sys.argv) >= 7:
		printLog = sys.argv[5].lower() == "true"

	#call main merge function
	merge(old_file, new_file, new_file_writeTo, delta, mark, printLog)
