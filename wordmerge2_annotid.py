import sys, os
import pandas as pd
import datetime
from shutil import move

## write functions based on audio or not audio

def create_merged(file_old, file_new, file_merged):
    bl_value = "***FIX ME***"
    old_error = False
    edit_word = False
    new_word = False

    old_df = pd.read_csv(file_old, keep_default_na=False)
    new_df = pd.read_csv(file_new, keep_default_na=False)

    merged_df = pd.DataFrame(columns = new_df.columns.values)
    #df = df.rename(columns={'oldName1': 'newName1'})
    for index, new_row in new_df.iterrows():

        word = ''
        to_add = new_row
        id = new_row['annotid']
        tmp = old_df[old_df['annotid']==id]
        # print(len(tmp.index))

        word = new_row['word']
        tier = new_row['tier']
        spk = new_row['speaker']
        utt_type = new_row['utterance_type']
        obj_pres = new_row['object_present']
        ts = new_row['timestamp']

        while len(tmp.index) != 0: # if the id already exists in the old df, check that the words/ts? do match

            if len(tmp.index) > 1:
                print("ERROR: annotid not unique in old version : ", id) # raise exception
                to_add['basic_level'] = bl_value
                merged_df = merged_df.append(to_add)
                old_error = True
                break
            old_row = tmp.iloc[0]



            # if new_row[:, new_row.columns != "basic_level"].equals(old_row[:, old_row.columns != "basic_level"]):
            if word == old_row['word']:
                # print("old", word)
                # check codes as well to know if something changed?
                to_add['basic_level'] = old_row['basic_level']
                merged_df = merged_df.append(to_add)
                break
            else:
                # print("old but different", word)
                to_add['basic_level'] = bl_value
                merged_df = merged_df.append(to_add)
                edit_word = True
                break

        else: # if the id is new: no info to retrieve, add row from new
            if word != '':
                # print("new", word)
                to_add['basic_level'] = bl_value
                merged_df = merged_df.append(to_add)
                new_word = True
                break
    # print(merged_df)
    merged_df.to_csv(file_merged)

    return old_error, edit_word, new_word


if __name__ == "__main__":

    home_visit_paths = sys.argv[1]

    old_error_list = []
    edit_word_list = []
    new_word_list = []

    today = str(datetime.datetime.now().year)+"_" \
            + str(datetime.datetime.now().month)+"_" \
            + str(datetime.datetime.now().day)+"_"
    with open(home_visit_paths, 'r') as f:
        lines = f.readlines()

    for line in lines:
        print(line)
        line = line.strip()

        # get name of old .csv file (with bl)+path to merged
        old_path = line+"/Analysis/Audio_Analysis/"
        for csv_file in os.listdir(old_path):
            if csv_file.endswith("audio_sparse_code.csv"):
                move(os.path.join(old_path, csv_file), os.path.join(old_path, "old_files", today+csv_file))
                old = os.path.join(old_path, "old_files", today+csv_file)
                out = os.path.join(old_path, csv_file)

        # get name of new .csv file (no bl)
        new_path = line+"/Coding/Audio_Annotation/"
        for csv_file in os.listdir(new_path):
            if csv_file.endswith("processed.csv"):
                new = os.path.join(new_path, csv_file)

        # compute merge
        if old and out and new:
            old_error, edit_word, new_word = create_merged(old, new, out)
            if old_error:
                old_error_list.append(line)
            if edit_word:
                edit_word_list.append(line)
            if new_word:
                new_word_list.append(line)

    # at the very end, write every error/change encountered
    with open("annotid_merge_errors.txt", "w+") as f:
        f.write("old_errors\n")
        for l in old_error_list:
            f.write(l+"\n")
        f.write("edit_word\n")
        for l in edit_word_list:
            f.write(l+"\n")
        f.write("new_word\n")
        for l in new_word_list:
            f.write(l+"\n")
