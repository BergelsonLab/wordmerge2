# wordmerge2

This is a repo for wordmerge2 python script and its folder version that merge basic level from old file to new file. 

- Both can be run directly in terminal or command line using python 2. 
- Both scripts require `pandas` python package installed.
- In order to run `wordmerge2_bash.py`, you need to have `wordmerge2.py` in the same folder. 
----
For `wordmerge2.py`, it accepts five inputs: *old_file*, *new_file*, *new_file_writeTo*, *delta*, *mark*

If no value given, *delta* and *mark* would be set to default 

- *old_file* is the path of the old file
- *new_file* is the path of the new file
- *new_file_writeTo* is the path of the wordmerge-processed file
- *delta* is the time range allowed for matching: 
  * When oldfile.timeOnset-*delta* < newfile.timeOnset < oldfile.timeOnset+*delta*, the pair would be considered with the same time stamp
  * Same is true for timeOffset
  * The default value for *delta* is 0
  * 
