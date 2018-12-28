'''
TODO
1. Read path
2. Open Home_Visit/Coding/Audio_Annotation/...sparse_code_processed.csv
    contains words - basic_level
3. Open Home_Visit/Analysis/Audio_Analysis/...audio_sparse_code.csv
    contains words - id
4. Merge the two on the words column
5. Save Home_Visit/Analysis/Audio_Analysis/...audio_sparse_code.csv
    as Home_Visit/Analysis/Audio_Analysis/...audio_sparse_code_no_id.csv
6. Save merged as Home_Visit/Analysis/Audio_Analysis/...audio_sparse_code.csv

'''

import sys
import os
import pandas as pd
from shutil import move

def create_merged(old_path, id_path, out_path):
    new_word = False
    # create dict word - basic level
    old = pd.read_csv(old_path, usecols = ["word", "basic_level"]).drop_duplicates()
    # change nan to NA here
    old = old.fillna("NA")
    # print(old)
    # read new csv (with id)
    new = pd.read_csv(id_path, usecols = ["tier", "word","utterance_type","object_present","speaker","annotid","timestamp"])
    # apply dict to new csv
    merged = new.merge(old, how='left', on='word')
    # add ***FIXME*** for words that were not in the old version
    if merged.isnull().sum().sum() !=0:
        new_word = True
    merged = merged.fillna("***FIXME***")
    merged = merged.drop_duplicates()
    # save new csv
    merged.to_csv(out_path, index=False)

    return new_word

def check_output(id_path, merged_path):
    new = pd.read_csv(id_path, usecols = ["tier", "word","utterance_type","object_present","speaker","annotid","timestamp"])
    out = pd.read_csv(merged_path, usecols = ["tier", "word","utterance_type","object_present","speaker","annotid","timestamp","basic_level"])
    # 1. check that merged has same number of rows as new
    row_count_new = len(new)
    row_count_out = len(out)
    # print(row_count_new, row_count_out)
    if row_count_new!=row_count_out:
        # a. open error file
        with open(os.path.join(merged_path.replace(".csv", "_error.txt")), "w+") as f:
        # b. write error message
            f.write("Different number of rows between processed and merged: processed="+str(row_count_new)+", merged="+str(row_count_out))
    return row_count_new==row_count_out



if __name__ == "__main__":

    home_visit_path = sys.argv[1]
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
        old_path = line+"/Analysis/Audio_Analysis/"
        for csv_file in os.listdir(old_path):
            if csv_file.endswith("audio_sparse_code.csv"):
                move(os.path.join(old_path, csv_file), os.path.join(old_path, csv_file.replace(".csv", "_no_id.csv")))
                old = os.path.join(old_path, csv_file.replace(".csv", "_no_id.csv"))
                out = os.path.join(old_path, csv_file)
        print(old, out)
        new = ""
        new_path = line+"/Coding/Audio_Annotation/"
        for csv_file in os.listdir(new_path):
            if csv_file.endswith("processed.csv"):
                new = os.path.join(new_path, csv_file)
    # old = sys.argv[1]
    # with_id = sys.argv[2]
    # out = sys.argv[3]
        if old and new and out:
            new_word = create_merged(old, new, out)
            if new_word:
                new_errors.append(old)
            check = check_output(new, out)
            if not check:
                count_errors.append(old)

        else:
            print(old, new, out)
            name_errors.append(old)

    with open("errors.txt", "w+") as f:
        f.write("count")
        for l in count_errors:
            f.write(l)
        f.write("new")
        for l in new_errors:
            f.write(l)
        f.write("name")
        for l in name_errors:
            f.write(l)
