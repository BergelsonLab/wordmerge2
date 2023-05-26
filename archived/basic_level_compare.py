import sys
import os
import pandas as pd
import csv
import time

#Read in the two all_basiclevel.csv files
#Write out 2 csv files: one with all of the rows common to both but had some...
#...value changed and one with the rows that exist in the first but not the 2nd

#Match against word, onset, tier (for audio), ordinal (for video)
#all 3 should match, can have option for 2/3- word, ord/tier

def compare_basic_level (arg):
    #Reading in arguments and checking them
    bigger_file = arg[0]
    smaller_file = arg[1]
    two_or_three = arg[2]
    two_or_three = int(two_or_three)
    assert two_or_three == 2 or two_or_three == 3, "Third argument must be 2 or 3"
    df_big = pd.read_csv(bigger_file, header = 0, keep_default_na = False)
    df_small = pd.read_csv(smaller_file, header = 0, keep_default_na = False)

    #Taking off the .csv extension of the filenames so combined filename doesn't have .csv in the middle of it
    bigger_file = bigger_file[:len(bigger_file) - 4]
    smaller_file = smaller_file[:len(smaller_file) - 4]
    
    #Combines data on either 2 or 3 properties
    if two_or_three == 2:
        print("Combining data...")
        combined_data = df_big.merge(df_small, how='outer', on=['ordinal', 'object', 'tier'], indicator = True)
        combined_data = combined_data.rename(columns={'_merge':'where_row'})
    else:
        print("Combining data...")
        combined_data = df_big.merge(df_small, how='outer', on=['ordinal', 'object', 'tier', 'onset'], indicator = True)
        combined_data = combined_data.rename(columns={'_merge': 'where_row'})

    #Create the only_big dataframe
    print("Creating the dataframe for rows only in bigger file...")
    only_big = combined_data[combined_data.where_row == "left_only"]
    

    #Match on 2/3 conditions
    print("Creating dataframe for rows found in both files...")
    common_rows = combined_data[combined_data.where_row == 'both']

    #Make a new big dataframe and a new small dataframe that each only have the rows that are common to both on account of matching on 2/3 values
    print("Making new big dataframe and new small dataframe...")
    #Need to check for 2/3 condition and take action accordingly
    if two_or_three == 2:
        new_bigger = common_rows.drop(['onset_y','offset_y', 'utterance_type_y', 'object_present_y', 'speaker_y', 'basic_level_y', 'id_y', 'subj_y', 'month_y', 'SubjectNumber_y', 'audio_video_y', 'where_row'], axis = 1)
        new_bigger = new_bigger.rename(columns = {'onset_x' : 'onset', 'offset_x':'offset', 'utterance_type_x':'utterance_type', 'object_present_x':'object_present', 'speaker_x':'speaker', 'basic_level_x':'basic_level', 'id_x':'id', 'subj_x':'subj', 'month_x':'month', 'SubjectNumber_x':'SubjectNumber', 'audio_video_x': 'audio_video'})
        new_smaller = common_rows.drop(['onset_x','offset_x', 'utterance_type_x', 'object_present_x', 'speaker_x', 'basic_level_x', 'id_x', 'subj_x', 'month_x', 'SubjectNumber_x', 'audio_video_x', 'where_row'], axis = 1)
        new_smaller = new_smaller.rename(columns = {'onset_y':'onset','offset_y':'offset', 'utterance_type_y':'utterance_type', 'object_present_y':'object_present', 'speaker_y':'speaker', 'basic_level_y':'basic_level', 'id_y':'id', 'subj_y':'subj', 'month_y':'month', 'SubjectNumber_y':'SubjectNumber', 'audio_video_y': 'audio_video'})
    else:
        new_bigger = common_rows.drop(['offset_y', 'utterance_type_y', 'object_present_y', 'speaker_y', 'basic_level_y', 'id_y', 'subj_y', 'month_y', 'SubjectNumber_y', 'audio_video_y', 'where_row'], axis = 1)
        new_bigger = new_bigger.rename(columns = {'offset_x':'offset', 'utterance_type_x':'utterance_type', 'object_present_x':'object_present', 'speaker_x':'speaker', 'basic_level_x':'basic_level', 'id_x':'id', 'subj_x':'subj', 'month_x':'month', 'SubjectNumber_x':'SubjectNumber', 'audio_video_x': 'audio_video'})
        new_smaller = common_rows.drop(['offset_x', 'utterance_type_x', 'object_present_x', 'speaker_x', 'basic_level_x', 'id_x', 'subj_x', 'month_x', 'SubjectNumber_x', 'audio_video_x', 'where_row'], axis = 1)
        new_smaller = new_smaller.rename(columns = {'offset_y':'offset', 'utterance_type_y':'utterance_type', 'object_present_y':'object_present', 'speaker_y':'speaker', 'basic_level_y':'basic_level', 'id_y':'id', 'subj_y':'subj', 'month_y':'month', 'SubjectNumber_y':'SubjectNumber', 'audio_video_y': 'audio_video'})

    cols = ['ordinal', 'onset', 'offset','object', 'utterance_type', 'object_present', 'speaker', 'basic_level', 'id', 'subj', 'month', 'SubjectNumber', 'audio_video', 'tier']
    new_smaller = new_smaller.reindex(columns = cols)

    #We have the common rows and what the values are for the smaller file, and we have the common rows and what the values are for the bigger file
    #Now, we match on all of the values and see which rows are different
    compare_matches = new_bigger.merge(new_smaller, how='outer', on=cols, indicator=True)
    compare_matches = compare_matches[compare_matches._merge != 'both']


    #What if you match on 2/3 conditions and then you make a new version of the big file and a new version of the small file that only have the rows that have been matched
    #Then, you merge the new small file and the new big file together on all of the values

    #Make the new filenames
    
    #combined_filename = "all_data_in_" + bigger_file + "_and_" + smaller_file + ".csv" ---If you want a file that has all of the data from both files in it
    compare_filename = "data_common_to_but_different_in_" + bigger_file + "_and_" + smaller_file + ".csv"
    only_big_filename = "data_only_in_" + bigger_file + "_and_not_" + smaller_file + ".csv"

    #Connvert dataframes to csv files
    print("Converting to csv...")
    #common_rows.to_csv("common_rows.csv", header = True, index = False) ---Shows matching on the two/three criteria
    #combined_data.to_csv(combined_filename, header = True, index= False) ---If you want a file that has all of the data from both files in it
    compare_matches.to_csv(compare_filename, header = True, index = False)
    only_big.to_csv(only_big_filename, header = True, index = False)
    #new_bigger.to_csv("bigger_df.csv", header = True, index = False) ---Shows the data in the big file on rows that are in both
    #new_smaller.to_csv("smaller_df.csv", header = True, index = False) ---Shows the data that's in the small file for the rows that are in both
    

if __name__ == "__main__":
    start = time.time()
    assert len(sys.argv) == 4, "Length of argument must be 4"
    big = sys.argv[1]
    small = sys.argv[2]
    two_or_three = sys.argv[3]

    compare_basic_level([big, small, two_or_three])
    end = time.time()
    print("Time elapsed: " + str(end-start)+" seconds")
        
    
