import sys
import csv

# Functions to check for video files

error_log = []
ordinal_list = []
total_lines = 0
acceptable_utterance_types = ['s', 'n', 'd', 'r', 'q', 'i']
acceptable_speaker = ['MOT', 'TOY', 'SIS', 'FAT', 'GRM', 'GRP']


def check_ordinal_video(ordinal, line_number):
    #Check for repeat values
    try:
        assert(not ordinal_list.contains(line_number))
    except AssertionError:
        error_log.append("Repeated ordinal value in line " + line_number)
        
    #Check for non-digit characters
    try:
        assert(x.isDigit() for x in ordinal)
    except AssertionError:
        error_log.append("Ordinal value is not a number in line " + line_number)

    digit_list = [0]
    digit_list.append(y for y in ordinal if y.isDigit())
    
    #Check that ordinal value is from 0 to total_lines-2, inclusive
    try:
        assert(int(''.join(digit_list) >= 0 and int('0'.join(digit_list) <= total_lines - 2)
    except AssertionError:
        error_log.append("Ordinal value out of bounds in line " + line_number)

    ordinal_list.append(ordinal)


def check_onset_video(onset, line_number):
    try:
        assert(x.isDigit() for x in onset)
    except AssertionError:
        error_log.append("Onset value is not a number in line " + line_number)


def check_offset_video(offset, line_number):
    try:
        assert(x.isDigit() for x in offset)
    except AssertionError:
        error_log.append("Offset value is not a number in line " + line_number)


def check_object_video(obj, line_number):
    for char in obj:
        try:
            assert (char.isalpha() or char == "+" or char == "'")
        except AssertionError:
            error_log.append("Object contains invalid character in line " + line_number)


def check_utterance_type_video(utterance_type, line_number):
    try:
        assert (utterance_type in acceptable_utterance_types)
    except:
        error_log.append("Utterance type invalid in line " + line_number)


def check_object_present_video(obj_pres, line_number):
    try:
        assert(obj_pres == "y" or obj_pres == "n")
    except:
        error_log.append("Object present invalid in line " + line_number)


def check_speaker_video(speaker, line_number):
    try:
        assert (speaker in acceptable_speaker)
    except:
        error_log.append("Speaker code invalid in line " + line_number)


def check_basic_level_video(basic_level, line_number):
    for char in basic_level:
        try:
            assert (char.isalpha() or char == "+" or char == "'")
        except AssertionError:
            error_log.append("Basic level contains invalid character in line " + line_number)


def give_error_report_video():
    # Loop through
    # Each entry is checked with a function above
    
    

    return 0


def check_word_audio():
    return "op"


def check_timestamp_audio():
    return 0


def check_tier_audio():
    return 0


def check_basic_level_audio():
    return 0


def give_error_report_audio():
    return 0


if name == __main__:
    check_object_video("hel'lo+")
