import sys
import csv
import pandas as pd
import codecheck
import os
import wordmerge2_func as wm2

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
    commonList = wm2.commonNA(common_file)

    if "word" in list(df_old):
		#cleanBL might be extra, haven't tested yet
        df_old = wm2.cleanBL(df_old, "basic_level")
        df_new = wm2.cleanBL(df_new, "basic_level")
        df_old = wm2.astDFAudio(df_old)
        df_new = wm2.astDFAudio(df_new)
        df_new, fixCount, caseCount, timeCount = wm2.getBasicAudio(df_old, df_new, mark, delta, commonList)
        isAudio = True
    else:
		#cleanBL might be extra, haven't tested yet
		df_old = wm2.cleanBL(df_old, "labeled_object.basic_level")
		df_new = wm2.cleanBL(df_new, "labeled_object.basic_level")
		df_new, fixCount, caseCount, timeCount = wm2.getBasicVideo(df_old, df_new, mark, delta, commonList)
		isAudio = False

	#generate wordmerged csv file
    newFileName = wm2.newpath(new_file, new_file_writeTo, "wordmerged.csv", isAudio)
    df_new.to_csv(newFileName, index = False)

    errorList = wm2.give_error_report(newFileName)

    logPath = wm2.newErrorPath(new_file, new_file_writeTo, "log.csv", isAudio)

    #Individual wordmerge run would print log to terminal by default, bash would turn this off
    if printLog:
    	wm2.printError(errorList, logPath)
    	wm2.printFix(fixCount, caseCount, timeCount)

    wm2.writeErrorLog(errorList, logPath, newFileName)

    return fixCount, caseCount, timeCount, isAudio, newFileName, errorList


#clean csv file for pandas reading
def clean(file):
	rowlist = list()
	with open(file, 'rU') as readfile:
		reader = csv.reader(readfile)
		rowlist = [l for l in reader]
        rlen = len(rowlist[0])
        for row in rowlist:
            if row[-1] == "":
                del row[-1]
            if len(row) > rlen:
                del row[rlen:]
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

# if __name__ == "__main__":
# 	#default value for last three inputs
# 	delta = 0
# 	mark = True
# 	printLog = True
#
# 	#input argument from terminal
# 	old_file = sys.argv[1]
# 	new_file = sys.argv[2]
# 	new_file_writeTo = sys.argv[3]
# 	if len(sys.argv) >= 5:
# 		delta = int(sys.argv[4])
# 	if len(sys.argv) >= 6:
# 		mark = sys.argv[5].lower() == "true"
# 	if len(sys.argv) >= 7:
# 		printLog = sys.argv[6].lower() == "true"
#
# 	#call main merge function
# 	merge(old_file, new_file, new_file_writeTo, delta, mark, printLog)
