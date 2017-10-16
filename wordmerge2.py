import sys
import csv
import re
import pandas as pd

#merge function rewrites the new_file with basic_level column 
#from old_file and returns dataframe of new_file
#parameters: old file path, new file path, error range allowed for timestemp, 
def merge(old_file, new_file, new_file_writeTo, delta, mark):
    print "merging {} --and-- {} .....".format(old_file, new_file)
    #clean csv file
    clean(new_file)
    clean(old_file)

    df_old = pd.read_csv(old_file, header = 0)
    df_new = pd.read_csv(new_file, header = 0)
    #df_old["basic_level"] = df_old["basic_level"].astype(str)
    #df_new["basic_level"] = df_new["basic_level"].astype(str)
    common_file = "common_words_index.csv"
    commonList = commonNA(common_file)
    if "word" in list(df_old):
    	df_old = cleanBL(df_old, "basic_level")
    	df_new = cleanBL(df_new, "basic_level")
    	df_new, fixCount, caseCount, timeCount = getBasicAudio(df_old, df_new, mark, delta, commonList)
    else:
    	df_old = cleanBL(df_old, "labeled_object.basic_level")
    	df_new = cleanBL(df_new, "labeled_object.basic_level")
    	df_new, fixCount, caseCount, timeCount = getBasicVideo(df_old, df_new, mark, delta, commonList)
    newFileName = newpath(new_file, new_file_writeTo)
    df_new.to_csv(newFileName, index = False)
    return fixCount, caseCount, timeCount

#get NA list
def commonNA(common_file):
	df_common = pd.read_csv(common_file, header = 0, usecols = [0, 1, 2, 3], keep_default_na = False)
	commonWord = df_common.loc[df_common["Basic Level"] == "NA", "word"]
	commonWord = [word.lower() for word in commonWord]
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

#get new_file_writeTo path
def newpath(new_file, new_file_writeTo):
	pathList = re.split('\\\|/', new_file)  #new_file.split("/") s
	newpathList = re.split("\\\|/", new_file_writeTo) #new_file_writeTo.split("/")
	fileName = pathList[-1]
	dateList = fileName.split("_")
	date = dateList[0] + "_" + dateList[1] + "_wordmerged.csv"
	fullName = ""
	for i in range(len(newpathList)):
		if ".csv" in newpathList[i]:
			continue
		fullName += newpathList[i]
		fullName += "/"
	fullName += date
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
		# for i in range(len(rowlist[0])):
		# 	if rowlist[0][i] == "labeled_object.basic_level":
		# 		rowlist[0][i] = "basic_level"
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
	for newr in df_new.index:
		df_old_lower = lowerDFVideo(df_old)
		try:
			temp_df = df_old_lower.loc[df_old_lower["labeled_object.object"] == df_new.get_value(newr, "labeled_object.object").lower(), ["labeled_object.offset", "labeled_object.onset", "labeled_object.basic_level"]]
			for oldr in temp_df.index:
				addMark = ""
 				if df_old.get_value(oldr, "labeled_object.object") != df_new.get_value(newr, "labeled_object.object"):
 					addMark = "*CASE*"
				if mark:
	 				addMark = df_old_lower.get_value(oldr, "labeled_object.basic_level") + addMark
	 				df_old_lower.set_value(oldr, "labeled_object.basic_level", addMark)
	 				temp_df.set_value(oldr, "labeled_object.basic_level", addMark)
			temp_df = temp_df.loc[temp_df["labeled_object.offset"] == df_new.get_value(newr, "labeled_object.offset"), ["labeled_object.basic_level", "labeled_object.onset"]]
			blValue = temp_df.loc[temp_df["labeled_object.onset"] == df_new.get_value(newr, "labeled_object.onset"), "labeled_object.basic_level"].values[0]
		except:
			blValue = getTimeChangeVideo(df_old_lower, newr, df_new, mark, delta)
		if "*CASE*" in blValue:
			caseCount += 1
		if "*TIME*" in blValue:
			timeCount += 1
		if blValue == "***FIX ME***":
			if df_new.get_value(newr, "labeled_object.object").lower() in commonList:
				blValue = "NA"
			else:
				fixCount += 1
		df_new.set_value(newr, "labeled_object.basic_level", blValue)
	return df_new, fixCount, caseCount, timeCount

#check if the timestamp is within the range
def getTimeChangeVideo(df_old_lower, newr, df_new, mark, delta):
	temp_df = df_old_lower.loc[df_old_lower["labeled_object.object"] == df_new.get_value(newr, "labeled_object.object").lower(), ["labeled_object.offset", "labeled_object.onset", "labeled_object.basic_level"]]
	if not temp_df.empty:
		blValue = "***FIX ME***"
		for oldr in temp_df.index:
			oldOnset = temp_df.get_value(oldr, "labeled_object.onset")
			oldOffset = temp_df.get_value(oldr, "labeled_object.offset")
			newOnset = df_new.get_value(newr, "labeled_object.onset")
			newOffset = df_new.get_value(newr, "labeled_object.offset")
			if abs(oldOnset - newOnset) <= delta and abs(oldOffset - newOffset) <= delta:
				blValue = temp_df.get_value(oldr, "labeled_object.basic_level")
				if mark:
					blValue = blValue + "*TIME*"
			else:
				continue
	else:
		blValue = "***FIX ME***"
	return blValue

#return the basic level entry with option to mark or not
def getBasicAudio(df_old, df_new, mark, delta, commonList):
	caseCount = 0
	fixCount = 0
	timeCount = 0
	for newr in df_new.index:
		df_old_lower = lowerDFAudio(df_old)
		try:
			temp_df = df_old_lower.loc[df_old_lower["tier"] == df_new.get_value(newr, "tier"), ["word", "timestamp", "basic_level"]]
 			temp_df = temp_df.loc[temp_df["word"] == df_new.get_value(newr, "word").lower(), ["basic_level", "timestamp", "word"]]
 			for oldr in temp_df.index:
 				addMark = ""
 				if df_old.get_value(oldr, "word") != df_new.get_value(newr, "word"):
 					addMark = "*CASE*"
 				if mark:
	 				addMark = df_old_lower.get_value(oldr, "basic_level") + addMark
	 				df_old_lower.set_value(oldr, "basic_level", addMark)
	 				temp_df.set_value(oldr, "basic_level", addMark)
 			blValue = temp_df.loc[temp_df["timestamp"] == df_new.get_value(newr, "timestamp"), "basic_level"].values[0]
		except:
			blValue = getTimeChangeAudio(df_old_lower, df_new, newr, mark, delta)
		if "*CASE*" in blValue:
			caseCount += 1
		if "*TIME*" in blValue:
			timeCount += 1
		if blValue == "***FIX ME***":
			if df_new.get_value(newr, "word").lower() in commonList:
				blValue = "NA"
			else:
				fixCount += 1
		df_new.set_value(newr, "basic_level", blValue)	
	return df_new, fixCount, caseCount, timeCount


#check if the timestamp is within the range
def getTimeChangeAudio(df_old_lower, df_new, newr, mark, delta):
	temp_df = df_old_lower.loc[df_old_lower["tier"] == df_new.get_value(newr, "tier"), ["word", "timestamp", "basic_level"]]
	temp_df = temp_df.loc[temp_df["word"] == df_new.get_value(newr, "word").lower(), ["basic_level", "timestamp"]]
	if not temp_df.empty:
		blValue = "***FIX ME***"
		for oldr in temp_df.index:
			oldTimestamp = temp_df.get_value(oldr, "timestamp").split("_")
			newTimestamp = df_new.get_value(newr, "timestamp").split("_")
			oldOnset = int(oldTimestamp[0])
			oldOffset = int(oldTimestamp[1])
			newOnset = int(newTimestamp[0])
			newOffset = int(newTimestamp[1])
			if abs(oldOnset - newOnset) <= delta and abs(oldOffset - newOffset) <= delta:
				blValue = temp_df.get_value(oldr, "basic_level")
				if mark:
					blValue = blValue + "*TIME*"
			else:
				continue

	else:
		blValue = "***FIX ME***"
	return blValue



if __name__ == "__main__":
	delta = 0
	mark = True

	old_file = sys.argv[1]
	new_file = sys.argv[2]
	new_file_writeTo = sys.argv[3]
	if len(sys.argv) >= 5:
		delta = int(sys.argv[4])
	if len(sys.argv) >= 6:
		mark = sys.argv[5].lower() == "true"

	merge(old_file, new_file, new_file_writeTo, delta, mark)
