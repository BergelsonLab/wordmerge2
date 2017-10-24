import sys
import csv

# Functions to check for video files
error_log = []
acceptable_utterance_types = ['s', 'n', 'd', 'r', 'q', 'i']

# THERE IS AN ISSUE WITH ROW NUMBERS NOT MATCHING UP PROPERLY
# It gives the line numbers properly for the new file but not the old file
# Also, the line numbers for the new file are repeated as the line numbers for the old file

def check_ordinal_video(ordinal, line_number, word, total_lines):

    #Having issues with checking for repeat values
    
    #Check for repeat values
    '''
    try:
        assert(not (line_number in ordinal_list))
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.ordinal repeat"])
    '''
        
    #Check for non-digit characters
    try:
        assert(x.isDigit() for x in ordinal)
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.ordinal"])

    digit_list = ['0']
    for y in ordinal:
        if y.isdigit():
            digit_list.append(y)
    string_of_digits = ''.join(digit_list)

    #Check that the ordinal number is in bounds
    try:
        assert(int(string_of_digits) >= 0 and int(string_of_digits) <= total_lines - 1)
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.ordinal"])

    #ordinal_list.append(ordinal)
    

def check_onset_video(onset, line_number, word):
    try:
        assert(x.isDigit() for x in onset)
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.onset"])


def check_offset_video(offset, line_number, word):
    try:
        assert(x.isDigit() for x in offset)
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.offset"])


def check_object_video(obj, line_number):
    for char in obj:
        try:
            assert (char.isalpha() or char == "+" or char == "'")
        except AssertionError:
            error_log.append([obj, line_number, "labeled_object.object"])


def check_utterance_type_video(utterance_type, line_number, word):
    try:
        assert (utterance_type in acceptable_utterance_types)
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.utterance_type"])


def check_object_present_video(obj_pres, line_number, word):
    try:
        assert(obj_pres == "y" or obj_pres == "n")
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.object_present"])


def check_speaker_video(speaker, line_number, word):
    if not len(speaker) == 3:
        error_log.append([word, line_number, "labeled_object.speaker"])
    for char in speaker:
        try:
            assert (char.isalpha() and char.isupper())
        except AssertionError:
            error_log.append([word, line_number, "labeled_object.speaker"])


def check_basic_level_video(basic_level, line_number, word):
    for char in basic_level:
        try:
            assert (char.isalpha() or char == "+" or char == "'")
        except AssertionError:
            error_log.append([word, line_number, "labeled_object.basic_level"])


def give_error_report_video(filepath):
    ordinal_list = []
    video_info = []
    with open(filepath, 'rt') as csvfileR:
        reader = csv.reader(csvfileR)
        for row in reader:
            video_info.append(row)

    total_lines = len(video_info)
    line_number = 1
    for row in video_info:
        if not line_number == 1:
            check_ordinal_video(row[0], str(line_number), row[3], total_lines)
            check_onset_video(row[1], str(line_number), row[3])
            check_offset_video(row[2], str(line_number), row[3])
            check_object_video(row[3], str(line_number))
            check_utterance_type_video(row[4], str(line_number), row[3])
            check_object_present_video(row[5], str(line_number), row[3])
            check_speaker_video(row[6], str(line_number), row[3])
            if len(row) > 7:
                check_basic_level_video(row[7], str(line_number), row[3])
        line_number += 1
    return error_log

#Functions to check for audio files

acceptable_tier = ['*CFP', '*CHF', '*CHN', '*CXF', '*CXN', '*FAF', '*FAN',
                   '*MAF', '*MAN', '*NON', '*OLF', '*OLN', '*SIL', '*TVF', '*TVN']

def check_tier_audio(tier, line_number, word):
    try:
        assert(tier in acceptable_utterance_types)
    except AssertionError:
        error_log.append([word, line_number, "tier"])


def check_word_audio(word, line_number):
    for char in word:
        try:
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
        assert(obj_pres == "y" or obj_pres == "n")
    except AssertionError:
        error_log.append([word, line_number, "object_present"])


def check_speaker_audio(speaker, line_number,word):
    if not len(speaker) == 3:
        error_log.append([word, line_number, "speaker"])
    for char in speaker:
        try:
            assert (char.isalpha() and char.isupper())
        except AssertionError:
            error_log.append([word, line_number, "speaker"])


def check_timestamp_audio(timestamp, line_number, word):
    underscore_index = timestamp.find("_")
    try:
        assert(underscore_index != -1)
    except AssertionError:
        error_log.append([word, line_number, "timestamp"])

    if underscore_index != -1:
        for x in range(len(timestamp)):
            if x != underscore_index:
               try:
                   assert(timestamp[x].isdigit())
               except AssertionError:
                   error_log.append([word, line_number, "timestamp"])
               
    

def check_basic_level_audio(basic_level, line_number, word):
    for char in basic_level:
        try:
            assert (char.isalpha() or char == "+" or char == "'")
        except AssertionError:
            error_log.append([word, line_number, "basic_level"])


def give_error_report_audio(filepath):
    audio_info = []
    with open(filepath, 'rt') as csvfileR:
        reader = csv.reader(csvfileR)
        for row in reader:
            audio_info.append(row)

    total_lines = len(audio_info)
    line_number = 1
    for row in audio_info:
        print("line number: " + str(line_number) + " word: " + row[1]) 
        if not line_number == 1:
            check_tier_audio(row[0], str(line_number), row[1])
            check_word_audio(row[1], str(line_number))
            check_utterance_type_audio(row[2], str(line_number), row[1])
            check_object_present_audio(row[3], str(line_number), row[1])
            check_speaker_audio(row[4], str(line_number), row[1])
            check_timestamp_audio(row[5], str(line_number), row[1])
            if len(row) > 6:
                check_basic_level_audio(row[6], str(line_number), row[1])
        line_number += 1
    return error_log


