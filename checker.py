import sys
import csv

# Functions to check for video files
error_log = []
acceptable_utterance_types = ['s', 'n', 'd', 'r', 'q', 'i', 'o', 'u']
acceptable_speaker_codes = ['MOT', 'FAT', 'CHI', 'BRO', 'SIS', 'GRM', 'GRP', 'GRA',
                            'GP2', 'AUN', 'AU2', 'UNC', 'UN2', 'FCO', 'FC2', 'MC2',
                            'TOY', 'TVN', 'MFT', 'MMT', 'MFV', 'MIS', 'MBR', 'MTY',
                            'MTV', 'MGM', 'MGP', 'MCU', 'MAF', 'FTY', 'FTV', 'FBR',
                            'FGM', 'FGP', 'FGA', 'FG2', 'FCU', 'FTS', 'SST', 'SCU',
                            'STY', 'BCU', 'BTY', 'MGG', 'FGG', 'GTY', 'GRY', 'GRO',
                            'CTY', 'ATY', 'UMT', 'ATV', 'CCU']
comment = "%com:"


def check_ordinal_video(ordinal, line_number, word, total_lines, ordinal_list):
    digit_list = ['0']
    for y in ordinal:
        if y.isdigit():
            digit_list.append(y)
    string_digits = ''.join(digit_list)
    int_digits = int(string_digits)
    
    try:
        #Check for repeat values
        assert(not (ordinal in ordinal_list))
        #Check for non-digit characters
        assert(x.isdigit() for x in ordinal)
        #Check that ordinal value is from 1 to total_lines-1, inclusive
        assert(int_digits >= 0 and int_digits <= total_lines - 1)

    except AssertionError:
        error_log.append([word, line_number, "labeled_object.ordinal"])

    ordinal_list.append(ordinal)
    

def check_onset_video(onset, line_number, word):
    try:
        assert(x.isdigit() for x in onset)
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.onset"])


def check_offset_video(offset, line_number, word):
    try:
        assert(x.isdigit() for x in offset)
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.offset"])


def check_object_video(obj, line_number):
    try:
    	if not obj.startswith(comment):
	        for char in obj:
	            assert (char.isalpha() or char == "+" or char == "'")
    except AssertionError:
        error_log.append([obj, line_number, "labeled_object.object"])


def check_utterance_type_video(utterance_type, line_number, word):
    try:
    	if word.startswith(comment):
    		assert (utterance_type == "NA")
    	else:
        	assert (utterance_type in acceptable_utterance_types)
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.utterance_type"])


def check_object_present_video(obj_pres, line_number, word):
    try:
    	if word.startswith(comment):
    		assert (obj_pres == "NA")
    	else:
        	assert(obj_pres == "y" or obj_pres == "n" or obj_pres == "o" or obj_pres == "u")
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.object_present"])


def isValid(speaker):
    if len(speaker) != 3: return False
    if speaker[0] == 'B' and speaker[1] == 'R' and speaker[2].isdigit():
        return True
    elif speaker[0] == 'S' and speaker[1] == 'I' and speaker[2].isdigit():
        return True
    elif speaker[0] == 'A' and speaker[1] == 'F' and speaker[2].isdigit():
        return True
    elif speaker[0] == 'A' and speaker[1] == 'M' and speaker[2].isdigit():
        return True
    elif speaker[0] == 'C' and speaker[1] == 'F' and speaker[2].isdigit():
        return True
    elif speaker[0] == 'C' and speaker[1] == 'M' and speaker[2].isdigit():
        return True
    elif speaker[0] == 'C' and speaker[1] == 'H' and speaker[2].isdigit():
        return True
    elif speaker[0] == 'E' and speaker[1] == 'F' and speaker[2].isalpha() and speaker[2].isupper():
        return True
    elif speaker[0] == 'E' and speaker[1] == 'M' and speaker[2].isalpha() and speaker[2].isupper():
        return True
    elif speaker[0] == 'B' and speaker[1] == 'S' and speaker[2].isalpha() and speaker[2].isupper():
        return True
    elif speaker[0] == 'A' and speaker[1] == 'F' and speaker[2].isalpha() and speaker[2].isupper():
        return True
    elif speaker[0] == 'A' and speaker[1] == 'M' and speaker[2].isalpha() and speaker[2].isupper():
        return True
    elif speaker[0] == 'C' and speaker[1] == 'F' and speaker[2].isalpha() and speaker[2].isupper():
        return True
    elif speaker[0] == 'C' and speaker[1] == 'M' and speaker[2].isalpha() and speaker[2].isupper():
        return True
    return False


def check_speaker_video(speaker, line_number, word):
	try:
            if word.startswith(comment):
		assert (speaker == "NA")
	    else:
		assert(len(speaker) == 3)
		assert((speaker in acceptable_speaker_codes) or isValid(speaker))
	except AssertionError:
		error_log.append([word, line_number, "labeled_object.speaker"])


def check_basic_level_video(basic_level, line_number, word):
    try:
    	if word.startswith(comment):
    	    assert (basic_level == "NA")
    	else:
	    for char in basic_level:
	        assert (char.isalpha() or char == "+" or char == "'" or char == " ")
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.basic_level"])


def give_error_report_video(filepath):
    global error_log
    error_log = []
    global ordinal_list
    ordinal_list = []
    video_info = []
    with open(filepath, 'rt') as csvfileR:
        reader = csv.reader(csvfileR)
        for row in reader:
            video_info.append(row)

    colName = video_info[0]
    for i in range(len(colName)):
        if colName[i] == "labeled_object.ordinal":
            ordinalI = i
        elif colName[i] == "labeled_object.onset":
            onsetI = i
        elif colName[i] == "labeled_object.offset":
            offsetI = i
        elif colName[i] == "labeled_object.utterance_type":
            utterI = i
        elif colName[i] == "labeled_object.object":
            objI = i
        elif colName[i] == "labeled_object.object_present":
            obj_preI = i
        elif colName[i] == "labeled_object.speaker":
            speakerI = i
        elif colName[i] == "labeled_object.basic_level" or colName[i] == "basic_level":
            basicI = i

    total_lines = len(video_info)
    line_number = 1
    for row in video_info:
        if not line_number == 1:
            check_ordinal_video(row[ordinalI], str(line_number), row[objI], total_lines, ordinal_list)
            check_onset_video(row[onsetI], str(line_number), row[objI])
            check_offset_video(row[offsetI], str(line_number), row[objI])
            check_object_video(row[objI], str(line_number))
            check_utterance_type_video(row[utterI], str(line_number), row[objI])
            check_object_present_video(row[obj_preI], str(line_number), row[objI])
            check_speaker_video(row[speakerI], str(line_number), row[objI])
            if len(row) > 7:
                check_basic_level_video(row[basicI], str(line_number), row[objI])
        line_number += 1
    return error_log

#Functions to check for audio files

acceptable_tier = ['*CHF', '*CHN', '*CXF', '*CXN', '*FAF', '*FAN', '*NOF',
                   '*MAF', '*MAN', '*NON', '*OLF', '*OLN', '*SIL', '*TVF', '*TVN']

def check_tier_audio(tier, line_number, word):
    try:
        assert(tier in acceptable_tier)
    except AssertionError:
        error_log.append([word, line_number, "tier"])


def check_word_audio(word, line_number):
    try:
        for char in word:
            assert (char.isalpha() or char == "+" or char == "'")
    except AssertionError:
        error_log.append([word, line_number, "word"])


def check_utterance_type_audio(utterance_type, line_number, word):
    try:
        assert (utterance_type in acceptable_utterance_types)
    except AssertionError:
        error_log.append([word, line_number, "utterance_type"])


def check_object_present_audio(obj_pres, line_number, word):
    try:
        assert(obj_pres == "y" or obj_pres == "n" or obj_pres == "u" or obj_pres == "o")
    except AssertionError:
        error_log.append([word, line_number, "object_present"])


def check_speaker_audio(speaker, line_number,word):
    if not len(speaker) == 3:
        error_log.append([word, line_number, "speaker"])
    else:
        try:
            for char in speaker:
                assert ((char.isalpha() and char.isupper()) or char.isdigit())
        except AssertionError:
            error_log.append([word, line_number, "speaker"])


def check_timestamp_audio(timestamp, line_number, word):
    underscore_index = timestamp.find("_")

    if underscore_index != -1:
        try:
            for x in range(len(timestamp)):
                if x != underscore_index:
                    assert(timestamp[x].isdigit())
        except AssertionError:
            error_log.append([word, line_number, "timestamp"])
    else:
        try:
            assert(underscore_index != -1)
        except AssertionError:
            error_log.append([word, line_number, "timestamp"])
               
    

def check_basic_level_audio(basic_level, line_number, word):
    try:
        for char in basic_level:
            assert (char.isalpha() or char == "+" or char == "'" or char == " ")
    except AssertionError:
        error_log.append([word, line_number, "basic_level"])


def give_error_report_audio(filepath):
    global error_log
    error_log = []
    audio_info = []
    with open(filepath, 'rt') as csvfileR:
        reader = csv.reader(csvfileR)
        for row in reader:
            audio_info.append(row)

    colName = audio_info[0]
    for i in range(len(colName)):
        if colName[i] == "tier":
            tierI = i
        elif colName[i] == "word":
            wordI = i
        elif colName[i] == "utterance_type":
            utterI = i
        elif colName[i] == "object_present":
            obj_preI = i
        elif colName[i] == "speaker":
            speakerI = i
        elif colName[i] == "timestamp":
            timestampI = i
        elif colName[i] == "basic_level":
            basicI = i

    line_number = 1
    for row in audio_info: 
        if not line_number == 1:
            check_tier_audio(row[tierI], str(line_number), row[wordI])
            check_word_audio(row[wordI], str(line_number))
            check_utterance_type_audio(row[utterI], str(line_number), row[wordI])
            check_object_present_audio(row[obj_preI], str(line_number), row[wordI])
            check_speaker_audio(row[speakerI], str(line_number), row[wordI])
            check_timestamp_audio(row[timestampI], str(line_number), row[wordI])
            if len(row) > 6:
                check_basic_level_audio(row[basicI], str(line_number), row[wordI])
        line_number += 1
    return error_log


