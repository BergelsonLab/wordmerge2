import sys
import csv

# Functions to check for video files

error_log = []
ordinal_list = []
total_lines = 0
acceptable_utterance_types = ['s', 'n', 'd', 'r', 'q', 'i']


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
        assert(int(''.join(digit_list)) >= 0 and int('0'.join(digit_list)) <= total_lines - 2)
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
    if not len(speaker) == 3:
        error_log.append("Speaker code invalid length in line " + line_number)
    for char in speaker:
        try:
            assert (char.isalpha() and char.isupper())
        except:
            error_log.append("Speaker code contains invalid character in line " + line_number)


def check_basic_level_video(basic_level, line_number):
    for char in basic_level:
        try:
            assert (char.isalpha() or char == "+" or char == "'")
        except AssertionError:
            error_log.append("Basic level contains invalid character in line " + line_number)


def give_error_report_video(filename):
    video_info = []
    with open(filename, 'rt') as csvfileR:
        reader = csv.reader(csvfileR, delimiter=',', quotechar='|')
        for row in reader:
            video_info.append(row)
    csvfileR.close()

    total_lines = len(video_info)
    line_number = 0
    for row in video_info:
        if not line_number == 0:
            check_ordinal_video(row[0], line_number)
            check_onset_video(row[1], line_number)
            check_offset_video(row[2], line_number)
            check_object_video(row[3], line_number)
            check_utterance_type_video(row[4], line_number)
            check_object_present_video(row[5], line_number)
            check_speaker_video(row[6], line_number)
            check_basic_level_video(row[7], line_number)
        line_number += 1
    return error_log


def check_tier_audio():
    return 0


def check_word_audio():
    return 0


def check_utterance_type_audio():
    return 0


def check_object_present_audio():
    return 0


def check_speaker_audio():
    return 0


def check_timestamp_audio():
    return 0


def check_basic_level_audio():
    return 0


def give_error_report_audio(filename):
    audio_info = []
    with open(filename, 'rt') as csvfileR:
        reader = csv.reader(csvfileR, delimiter=',', quotechar='|')
        for row in reader:
            audio_info.append(row)
    csvfileR.close()

    total_lines = len(audio_info)
    line_number = 0
    for row in audio_info:
        if not line_number == 0:
            check_tier_audio(row[0], line_number)
            check_word_audio(row[1], line_number)
            check_utterance_type_audio(row[2], line_number)
            check_object_present_audio(row[3], line_number)
            check_speaker_audio(row[4], line_number)
            check_timestamp_audio(row[5], line_number)
            check_basic_level_audio(row[6], line_number)
        line_number += 1
    return error_log


