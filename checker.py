import sys
import csv

# Functions to check for video files

error_log = []
ordinal_list = []
total_lines = 0


def check_ordinal_video(ordinal, line_number):

    # Ordinal should be a number from 0 to number of lines - 2, inclusive
    try:
        assert(not ordinal_list.contains(line_number))
    except AssertionError:
        error_log.append("Repeated ordinal value in line " + line_number)

    try:
        assert(x.isDigit() for x in ordinal)
    except AssertionError:
        error_log.append("Ordinal value is not a number in line " + line_number)

    digit_list = [0]
    digit_list.append(y for y in ordinal if y.isDigit())

    try:
        assert(int(''.join(digit_list) >= 0 and int('0'.join(digit_list) <= total_lines - 2)
    except AssertionError:
        error_log.append("Ordinal value out of bounds in line " + line_number)

    ordinal_list.append(ordinal)


def check_onset_video():
    return 0


def check_offset_video():
    return 0


def check_object_video(object, line_number):
    for char in object:
        try:
            assert (char.isalpha() or char == "+" or char == "'")
        except AssertionError:
            error_log.append("Error with object in line " + line_number)


def check_utterance_type_video(object, line_number):
    return 0


def check_object_present_video(object, line_number):
    return 0


def check_speaker_video(object, line_number):
    return 0


def check_basic_level_video():
    return 0


def give_error_report_video():
    # Could loop through the entire dataframe
    # Each entry is checked with a function above
    # Can try/except to print out that there was an error at entry number i
    # Could use assert

    # Functions to check for audio files
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
