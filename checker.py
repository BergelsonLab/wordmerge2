import sys
import csv
import codecheck

error_log = []

#get error log for video file
def give_error_report_video(info):
    global error_log
    error_log = []
    global ordinal_list
    ordinal_list = []
    video_info = info


    #get index for each column
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

    #check each column from each row
    total_lines = len(video_info)
    line_number = 1
    for row in video_info:
        if not line_number == 1:

            if not codecheck.check_ordinal_video(row[ordinalI], total_lines, ordinal_list):
                error_log.append([row[objI], str(line_number), "labeled_object.ordinal"])
            ordinal_list.append(row[ordinalI])

            if not codecheck.check_onset_video(row[onsetI]):
                error_log.append([row[objI], str(line_number), "labeled_object.onset"])

            if not codecheck.check_offset_video(row[offsetI]):
                error_log.append([row[objI], str(line_number), "labeled_object.offset"])

            if not codecheck.check_object_video(row[objI]):
                error_log.append([row[objI], str(line_number), "labeled_object.object"])

            if not codecheck.check_utterance_type_video(row[utterI], row[objI]):
                error_log.append([row[objI], str(line_number), "labeled_object.utterance_type"])

            if not codecheck.check_object_present_video(row[obj_preI], row[objI]):
                error_log.append([row[objI], str(line_number), "labeled_object.object_present"])

            if not codecheck.check_speaker_video(row[speakerI], row[objI]):
                error_log.append([row[objI], str(line_number), "labeled_object.speaker"])

            #check basic level when there is one
            if len(row) > 7:
                if not codecheck.check_basic_level_video(row[basicI], row[objI]):
                    error_log.append([row[objI], str(line_number), "labeled_object.basic_level"])

        line_number += 1
    return error_log


#get error log for video file
def give_error_report_audio(info):
    global error_log
    error_log = []
    audio_info = info


    #get index for each column
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

    #check each column from each row
    line_number = 1
    for row in audio_info: 
        if not line_number == 1:
            if not codecheck.check_tier_audio(row[tierI]):
                error_log.append([row[wordI], str(line_number), "tier"])
            
            if not codecheck.check_word_audio(row[wordI]):
                error_log.append([row[wordI], str(line_number), "word"])
            
            if not codecheck.check_utterance_type_audio(row[utterI]):
                error_log.append([row[wordI], str(line_number), "utterance_type"])

            if not codecheck.check_object_present_audio(row[obj_preI]):
                error_log.append([row[wordI], str(line_number), "object_present"])

            if not codecheck.check_speaker_audio(row[speakerI]):
                error_log.append([row[wordI], str(line_number), "speaker"])
            
            if not codecheck.check_timestamp_audio(row[timestampI]):
                error_log.append([row[wordI], str(line_number), "timestamp"])

            #check basic level when there is one
            if len(row) > 6:
            	if not codecheck.check_basic_level_audio(row[basicI]):
                	error_log.append([row[wordI], str(line_number), "basic_level"])

        line_number += 1
    return error_log

# read in csv file and call the right function based on the file type
def give_error_report(filepath):
    info = []
    with open(filepath, 'rt') as csvfileR:
        reader = csv.reader(csvfileR)
        for row in reader:
            info.append(row)

    if "word" in info[0]:
        error_log = give_error_report_audio(info)
    else:
        error_log = give_error_report_video(info)

    return error_log


