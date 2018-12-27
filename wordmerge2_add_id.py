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
import pandas as pd

def create_merged(old_path, id_path, out_path):
    # create dict word - basic level
    old = pd.read_csv(old_path, usecols = ["word", "basic_level"]).drop_duplicates()
    # read new csv (with id)
    new = pd.read_csv(id_path, usecols = ["tier", "word","utterance_type","object_present","speaker","annotid","timestamp"])
    # apply dict to new csv
    merged = new.merge(old, on='word')
    # save dict
    merged.to_csv(out_path, index=False)

def check_output(new, merged):
    # check that merged has same number of rows as new
    # check that all rows have basic level -- except for those where words were added, which are?


if __name__ == "__main__":
    old = sys.argv[1]
    with_id = sys.argv[2]
    out = sys.argv[3]
    create_merged(old, with_id, out)
