# wordmerge2

This is a repo for wordmerge2 python script and its folder version that merges basic level from old file to new file in a newly-generated csv file. 

- Both can be run directly in terminal or command line using python 2. 
- Both scripts require `pandas` python package installed.
- In order to run `wordmerge2_bash.py`, you need to have `wordmerge2.py` in the same folder. 
- In order to run `wordmerge2_bash.py` and `wordmerge2.py`, you need to have `common_words_index.csv` in the same folder. 
----
## wordmerge2.py

For `wordmerge2.py`, it accepts six inputs: *old_file*, *new_file*, *new_file_writeTo*, *delta*, *mark* and *printLog*

A new csv file would be generated as the merged version with the name `prefix_wordmerged.csv`, with prefix from the file pair. 

For every row in the new file, the script will run through the old file and find the matching row with same object name/word and timestamp (also tier for audio file). If no row in the old file matches up, this row would be marked `***FIX ME***` in the merged csv file. 

The file pairs would not be changed (although the extra space might be cleaned), all the changes would occur in the merged csv file. 

If the script does not recieve the last three input, *delta*, *mark* and *printLog* would be set to default 

- *old_file* is the path of the old file
- *new_file* is the path of the new file
- *new_file_writeTo* is the path of folder in which the wordmerge-processed file will be generated
- *delta* is the time range allowed for matching: 
  * When oldfile.timeOnset-*delta* < newfile.timeOnset < oldfile.timeOnset+*delta*, the pair would be considered with the same time stamp
  * Same is true for timeOffset
  * The default value for *delta* is 0
  * When the timestamp does not match up perfectly from the old file to the new file but within the range of delta, `*TIME*` would be added to the basic_level column when *mark* is set to `True`
- *mark* turns on and off the marking for case change and time in range for basic_level column
  * When *mark* is `True`, `*TIME*` will be added to basic_level column if the timestamp is not the same but inside the range, `*CASE*` will be added to basic_level column if the object names/words match only when changing the case. 
  * When *mark* is `False`, rows from old file and new file would still be paired together when timestamps are inside the range or object names/words have difference case, but no mark would occur in the basic_level column. 
  * The default value for *mark* is `True`. 
- *printLog* turns on and off the printing of log information to terminal or commandline
  * When *printLog* is `True`, error and count log information would be printed to terminal or commandline
  * When *printLog* is `False`, log information would be silenced
  * The default value for *printLog* is `True`. 
  
---
## wordmerge2_bash.py
For `wordmerge2_bash.py`, it accepts two inputs: *old_folder* and *new_folder*

This script runs `wordmerge2.py` for every pair of files that have the same prefix inside the old folder and prints new csv files to the new folder. 

Two log files will also be generated in the new folder. `date_count_log.csv` records the counts for the occurrence of `***FIX ME***`, `*CASE*` and `*TIME*`; `date_error_log.csv` records the counts of errors in different types for each file. 

*delta* and *mark* inputs are set to default value inside this script, *printLog* is set to False so no individual log information would be printed to terminal or commandline, but the total count log would be displayed. 

- *old_folder* is the path of the old folder which contains both old files and new files and should be absolute path. 
- *new_folder* is the path of the new folder where merged csv files are generated and should be absolute path. 
