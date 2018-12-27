import sys
import os
from shutil import move
import wordmerge2_add_id as wm_id


# 1. clean "with_id"
# 2. wordmerged => audio_sparse_code => merge

if __name__ == "__main__":

    home_visit_paths = sys.argv[1]

    with open(home_visit_paths, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        old_path = line+"/Analysis/Audio_Analysis/"

        for csv_file in os.listdir(old_path):
            # if done but bad naming
            if csv_file.endswith("audio_sparse_code_with_id.csv"):
                os.remove(os.path.join(old_path, csv_file))
            if csv_file.endswith("audio_sparse_code_no_id.csv"):
                move(os.path.join(old_path, csv_file), os.path.join(old_path+"/old_files/", csv_file))
            # if not done because of wordmerged name
            if csv_file.endswith("wordmerged.csv"):
                print("wordmerged", line)
                move(os.path.join(old_path, csv_file), os.path.join(old_path, csv_file.replace("wordmerged", "sparse_code_no_id")))
                # do merge
                # rename the old/name output
                old = os.path.join(old_path, csv_file.replace("wordmerged", "sparse_code_no_id"))
                out = os.path.join(old_path, csv_file.replace("wordmerged", "sparse_code"))
                # get the new
                new_path = line+"/Coding/Audio_Annotation/"
                for csv_file in os.listdir(new_path):
                    if csv_file.endswith("processed.csv"):
                        new = os.path.join(new_path, csv_file)
                if old and new and out:

                    new_word = wm_id.create_merged(old, new, out)
                    check = wm_id.check_output(new, out)
                    print(line, new_word, check)
                else:
                    print("ERROR TO FIX", line)

        # checking presence of audio_sparse_code
        ok = False
        for csv_file in os.listdir(old_path):
            if csv_file.endswith("audio_sparse_code.csv"):
                ok = True
        if not ok:
            print("NOT OK", line)
