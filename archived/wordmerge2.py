import wordmerge2_batch as batch
import wordmerge2_pho as pho
import wordmerge2_bl as bl
import sys


if __name__ == "__main__":
	#default value for last three inputs
	delta = 0
	mark = True
	printLog = True

	#input argument from terminal
	if "-batch" in sys.argv:
		old_folder = sys.argv[1]
		new_folder = sys.argv[2]
		if "-pho" in sys.argv:
			batch.runWordmerge2(old_folder, new_folder, True)
		else:
			batch.runWordmerge2(old_folder, new_folder, False)
	else:
		old_file = sys.argv[1]
		new_file = sys.argv[2]
		new_file_writeTo = sys.argv[3]
		if len(sys.argv) >= 5 and not sys.argv[4].startswith("-"):
			delta = int(sys.argv[4])
		if len(sys.argv) >= 6 and not sys.argv[5].startswith("-"):
			mark = sys.argv[5].lower() == "true"
		if len(sys.argv) >= 7 and not sys.argv[6].startswith("-"):
			printLog = sys.argv[6].lower() == "true"
		if "-pho" in sys.argv:
			pho.merge(old_file, new_file, new_file_writeTo, delta, mark, printLog)
		else:
			bl.merge(old_file, new_file, new_file_writeTo, delta, mark, printLog)
