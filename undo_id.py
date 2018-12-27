import sys
import os
from shutil import move


if __name__ == "__main__":

    home_visit_paths = sys.argv[1]

    with open(home_visit_paths, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        old_path = line+"/Analysis/Audio_Analysis/"

        for csv_file in os.listdir(old_path):
            if csv_file.endswith("audio_sparse_code.csv"):
                move(os.path.join(old_path, csv_file), os.path.join(old_path, csv_file.replace(".csv", "_with_id.csv")))
        for csv_file in os.listdir(old_path):
            if csv_file.endswith("audio_sparse_code_no_id.csv"):
                move(os.path.join(old_path, csv_file), os.path.join(old_path, csv_file.replace("_no_id.csv", ".csv")))
