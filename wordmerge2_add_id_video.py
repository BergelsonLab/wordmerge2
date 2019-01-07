'''
TODO
1. Read path
2. Open Home_Visit/Coding/Video_Annotation/...processed.csv
    /!\\ rename output of opf2csv.py
    contains words - basic_level
3. Open Home_Visit/Analysis/Video_Analysis/...video_sparse_code.csv
    hopefully all named this way
    contains words - id
4. Copy new in merged, create dictionary of word-bl based on old and fill basic level column in merged
5. Save Home_Visit/Analysis/Video_Analysis/...video_sparse_code.csv
    as Home_Visit/Analysis/Video_Analysis/...video_sparse_code_no_id.csv
6. Save merged as Home_Visit/Analysis/Video_Analysis/...video_sparse_code.csv

'''

import sys
import os
import pandas as pd
from shutil import move

def create_merged(old_path, id_path, out_path):
    new_word = False
    # create dict word - basic level
    try:
        old = pd.read_csv(old_path, usecols = ["labeled_object.object", "labeled_object.basic_level"]).drop_duplicates()
    except ValueError:
        old = pd.read_csv(old_path, usecols = ["labeled_object.object", "basic_level"]).drop_duplicates()
        # df = df.rename(columns={'oldName1': 'newName1'
        old.columns=["labeled_object.object", "labeled_object.basic_level"]
    # change nan to NA here
    old = old.fillna("NA")
    # print(old)
    # read new csv (with id)
    new = pd.read_csv(id_path, usecols = ["labeled_object.ordinal", "labeled_object.onset", "labeled_object.offset", "labeled_object.object", "labeled_object.utterance_type", "labeled_object.object_present", "labeled_object.speaker", "labeled_object.id", "basic_level"])
    new = new.loc[~new["labeled_object.object"].str.contains("%")]
    # apply dict to new csv
    merged = new.merge(old, how='left', on='labeled_object.object')
    merged = merged.drop(["basic_level"], axis = 1)
    # add ***FIXME*** for words that were not in the old version
    if merged.isnull().sum().sum() !=0:
        print(merged.isnull().sum().sum())
        new_word = True
    values = {'labeled_object.basic_level':'***FIXME***', "labeled_object.id":"***NOID***"}
    merged = merged.fillna(value=values)
    # TODO check here if fixme at the wrong place?
    merged = merged.drop_duplicates()

    # save new csv
    merged.to_csv(out_path, index=False)

    return new_word, len(merged)==len(new)

def check_output(id_path, merged_path):
    print("check")
    new = pd.read_csv(id_path, usecols = ["labeled_object.ordinal", "labeled_object.onset", "labeled_object.offset", "labeled_object.object", "labeled_object.utterance_type", "labeled_object.object_present", "labeled_object.speaker", "labeled_object.id"])
    new = new.loc[~new["labeled_object.object"].str.contains("%")]
    out = pd.read_csv(merged_path, usecols = ["labeled_object.ordinal", "labeled_object.onset", "labeled_object.offset", "labeled_object.object", "labeled_object.utterance_type", "labeled_object.object_present", "labeled_object.speaker", "labeled_object.id", "labeled_object.basic_level"])
    # 1. check that merged has same number of rows as new
    row_count_new = len(new)
    row_count_out = len(out)
    print(row_count_new, row_count_out)
    if row_count_new!=row_count_out:
        # a. open error file
        with open(os.path.join(merged_path.replace(".csv", "_error.txt")), "w+") as f:
        # b. write error message
            print(os.path.join(merged_path.replace(".csv", "_error.txt")))
            f.write("Different number of rows between processed and merged: processed="+str(row_count_new)+", merged="+str(row_count_out))
    return row_count_new==row_count_out



if __name__ == "__main__":

    home_visit_path = sys.argv[1] # file containing path to all the home_visit existing in the database
    opf_csv_path = sys.argv[2] # path to all csv from opf files
    # output = sys.argv[2]
    count_errors = []
    name_errors = []
    new_errors = []

    with open(home_visit_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        old = ""
        out = ""
        old_path = line+"/Analysis/Video_Analysis/"
        for csv_file in os.listdir(old_path):
            if csv_file.endswith("video_sparse_code.csv"):
                move(os.path.join(old_path, csv_file), os.path.join(old_path, csv_file.replace(".csv", "_no_id.csv")))
                old = os.path.join(old_path, csv_file.replace(".csv", "_no_id.csv"))
                out = os.path.join(old_path, csv_file)
        print(old, out)
        new = ""

        # new_path = line+"/Coding/Video_Annotation/"
        subject = line.strip("/").split("/")[-2] # last one is Home_Visit
        print(subject)
        for csv_file in os.listdir(opf_csv_path):
            if csv_file.endswith("processed.csv") and subject in csv_file:
                new = os.path.join(opf_csv_path, csv_file)
                break
    # old = sys.argv[1]
    # with_id = sys.argv[2]
    # out = sys.argv[3]
        if old and new and out:
            new_word, check = create_merged(old, new, out)
            if new_word:
                new_errors.append(old)
            check = check_output(new, out)
            if not check:
                count_errors.append(old)

        else:
            print(old, new, out)
            name_errors.append(old)

    with open("video_errors.txt", "w+") as f:
        f.write("count")
        for l in count_errors:
            f.write(l)
        f.write("new")
        for l in new_errors:
            f.write(l)
        f.write("name")
        for l in name_errors:
            f.write(l)
