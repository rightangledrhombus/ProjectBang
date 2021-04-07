import os
import subprocess
import ffmpeg
import json
import re

def main():

    credits_length = 31.0
    intro_length = 30.0
    in_filename = "Z:\The Big Bang Theory S01-S10 (2007-)\The Big Bang Theory S02 (360p re-blurip)\The Big Bang Theory S02E01 The Bad Fish Paradigm.mp4"
    #in_filename = "G:\Plex\The Big Bang Theory\The Big Bang Theory S01-S10 (2007-)\The Big Bang Theory S02 (360p re-blurip)\The Big Bang Theory S02E01 The Bad Fish Paradigm.mp4"
    intro_screenshot = "Z:\snapshots\s02e01_intro.jpg"
    in_filename_split = os.path.splitext(in_filename)
    out_filename = in_filename_split[0] + "_trim" + in_filename_split[1]

    # get total time in video    
    probe = ffmpeg.probe(in_filename)
    total_duration = float(probe['format']['duration'])

    # calculate new end time for trimmed video
    end_time = total_duration - credits_length
    
    intro_start = find_intro_time(in_filename, intro_screenshot)

    #trim credits
    input = ffmpeg.input(in_filename) \
                .trim(start=0.0, end=end_time) \
                .output(out_filename) \
                .run()
   
    #clip out credits and create trimmed video
    subprocess.check_output("ffmpeg.exe -i %s -ss 00 -to %s %s" % (input_file, end_time, out_file))

''' Returns the timestamp in a video that matches a screenshot '''
def find_intro_time(in_filename, screenshot):

    """ find all matching frames for the screenshot.
        -ss = start time
        -t = search time 
        blackframe = amount of pixels matching the screenshot in each frame e.g. 99:32. 99% of pixels are less than
        returns a large string of information."""
    subprocess_result = subprocess.getoutput("ffmpeg.exe -ss 200 -t 100 -i \"%s\" -loop 1 -i \"%s\" -an -filter_complex \"[0]extractplanes=y[v];[1]extractplanes=y[i];[v][i]blend=difference:shortest=1,blackframe=99:32\" -f null -" % (in_filename, intro_jpeg_filename))

    # find floating point number in string that is after " t:". e.g. " t:50.2424". This is the timestamp of the frames that match the image.
    # take the first one in case of multiple matches.
    intro_start_time = re.compile(' t:(\d+\.\d+)').findall(subprocess_result)[0]

    return intro_start_time

if __name__ == "__main__":
    main()