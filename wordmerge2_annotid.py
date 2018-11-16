import sys
import pandas as pd

if __name__ = "__main__""

    file_old = sys.argv[1]
    file_new = sys.argv[2]
    file_merged = sys.argv[3]

    bl_value == "***FIX ME***"

    old_df = pd.read_csv(file_old)
    new_df = pd.read_csv(file_new)

    merged_df = pd.DataFrame(columns = new_df.columns.values)

    for index, new_row in new_df.iterrows():

        to_add = new_row
        id = new_row['annotid']
        tmp = old_df[old_df['annotid']==id]

        if len(tmp.index) != 0: # if the id already exists in the old df, check that the words/ts do match
            if len(tmp.index) > 1:
                print("ERROR: annotid not unique in old version")
            old_row = tmp.iloc[0]

            word = new_row['word']
            tier = new_row['tier']
            spk = new_row['speaker']
            utt_type = new_row['utterance_type']
            obj_pres = new_row['object_present']
            ts = new_row['timestamp']

            if new_row[:, new_row.columns != "basic_level"].equals(old_row[:, old_row.columns != "basic_level"]):
                merged_df.append(old_row)


        else: # if the id is new: no info to retrieve, add row from new

            to_add['basic_level'] = bl_value
            merged_df.append(to_add)
