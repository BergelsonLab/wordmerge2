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
def merge(bl_file, pho_file, new_file_writeTo, delta, mark, printLog):
    print "\n" + "merging {} --and-- {} .....".format(old_file, new_file) + "\n"
    #clean csv file
    clean(bl_file)
    clean(pho_file)

    df_bl = pd.read_csv(bl_file, header = 0, keep_default_na=False)
    df_pho = pd.read_csv(pho_file, header = 0, keep_default_na=False)
    df_bl = astDFAudio(df_bl)
    df_pho = astDFAudio(df_pho)
    df_new = copyPho(df_pho)

    if "word" in list(df_bl):
		#cleanBL might be extra, haven't tested yet
		df_bl = wm2.cleanBL(df_bl, "basic_level")
		df_new = wm2.cleanBL(df_new, "basic_level")
		df_final, fixCount, caseCount, timeCount = wm2.getBasicAudio(df_bl, df_new, mark, delta, commonList)
		isAudio = True
    else:
		#cleanBL might be extra, haven't tested yet
		df_bl = wm2.cleanBL(df_bl, "labeled_object.basic_level")
		df_new = wm2.cleanBL(df_new, "labeled_object.basic_level")
		df_final, fixCount, caseCount, timeCount = wm2.getBasicVideo(df_bl, df_new, mark, delta, commonList)
		isAudio = False

    common_file = "common_words_index.csv"
    commonList = wm2.commonNA(common_file)

    # if not outputPho:
    #     df_new = copyBL(df_bl)
    #     newFileName = newpath(bl_file, new_file_writeTo, "wordmerged.csv")
    #     logPath = newErrorPath(bl_file, new_file_writeTo, "log.csv")
    #     df_final, fixCount, caseCount, timeCount = getBasicAudio(df_pho, df_new, mark, delta, commonList)
    # else:
    newFileName = wm2.newpath(pho_file, new_file_writeTo, "wordmerged.csv")
    logPath = wm2.newErrorPath(pho_file, new_file_writeTo, "log.csv")


	#generate wordmerged csv file
    df_final.to_csv(newFileName, index = False)

    errorList = wm2.give_error_report(newFileName)

    #Individual wordmerge run would print log to terminal by default, bash would turn this off
    if printLog:
    	wm2.printError(errorList, logPath)
    	wm2.printFix(fixCount, caseCount, timeCount)

    wm2.writeErrorLog(errorList, logPath, newFileName)

    return fixCount, caseCount, timeCount, isAudio, newFileName, errorList

#make a copy of basiclevel df and add pho column
def copyBL(df):
    out_df = df.copy()
    colArr = out_df.columns.values
    if "pho" not in colArr:
        out_df["pho"] = ""
    return out_df

#make a copy of pho df and add BL column
def copyPho(df):
    out_df = df.copy()
    colArr = out_df.columns.values
    if "basic_level" not in colArr:
        out_df["basic_level"] = ""
    return out_df

#get rid of asterisk in tier/add asterisk
def astDFAudio(df):
	df_ast = df
	for r in range(0, len(df_ast.index)):
		tier = df_ast.get_value(r, "tier")
        df_ast.set_value(r, "tier", tier.replace("*", ""))
	return df_ast

#clean csv file for pandas reading
def clean(file):
	rowlist = list()
	with open(file, 'rU') as readfile:
		reader = csv.reader(readfile)
		rowlist = [l for l in reader]
		for row in rowlist:
			if row[-1] == "":
				del row[-1]
	with open(file, 'wb') as writefile:
		writer = csv.writer(writefile)
		for n in rowlist:
			writer.writerow(n)


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
		outputPho = sys.argv[4].lower() == "true"
	if len(sys.argv) >= 6:
		delta = int(sys.argv[5])
	if len(sys.argv) >= 7:
		mark = sys.argv[6].lower() == "true"
	if len(sys.argv) >= 8:
		printLog = sys.argv[7].lower() == "true"

	#call main merge function
	merge(old_file, new_file, new_file_writeTo, outputPho, delta, mark, printLog)
