import sys
import os
import pandas as pd
import csv

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
    else:
        print("Combining data...")
        combined_data = df_big.merge(df_small, how='outer', on=['ordinal', 'object', 'tier', 'onset'], indicator = True)
    
    print("Making dataframes...")
    #Make empty dataframes
    common = pd.DataFrame()
    only_big = pd.DataFrame()
    
    #Loop through combined datasets and fill the dataframes
    count = 0
    both_count = 0
    print("Looping through")
    for index, row in combined_data.iterrows():
        if count == 0:
            common = common.append(row)
            only_big = only_big.append(row)
        elif row[len(row)-1] == "both":
            both_count += 1
            common = common.append(row)
        elif row[len(row)-1] == "left_only":
            only_big = only_big.append(row)
        count += 1

    #Make the new filenames
    combined_filename = "all_data_in_" + bigger_file + "_and_" + smaller_file + ".csv"
    common_filename = "data_common_to" + bigger_file + "_and_" + smaller_file + ".csv"
    only_big_filename = "data_only_in_" + bigger_file + "_and_not_" + smaller_file + ".csv"

    #Connvert dataframes to csv filess
    print("Convert to csv")
    combined_data.to_csv(combined_filename, header = True)
    print("Convert to csv")
    common.to_csv(common_filename, header = True)
    print("Convert to csv")
    only_big.to_csv(only_big_filename, header = True)
    

if __name__ == "__main__":
    assert len(sys.argv) == 4, "Length of argument must be 4"
    big = sys.argv[1]
    small = sys.argv[2]
    two_or_three = sys.argv[3]

    compare_basic_level([big, small, two_or_three])
        
    