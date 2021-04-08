import os
import subprocess
import ffmpeg
import re

def main():

    parent_dir = "Z:\The Big Bang Theory S01-S10 (2007-)\season12_temp"
    files_path = [os.path.join(r,file) for r,d,f in os.walk(parent_dir) for file in f]

    for in_filename in files_path:
        in_filename_split = os.path.splitext(in_filename)
        out_filename = in_filename_split[0] + "_trim" + in_filename_split[1]
        
        trim_video(in_filename, out_filename)   


def trim_video(in_filename, out_filename):
    
    intro_screenshot = "Z:\snapshots\s12_intro.jpg"
    credits_screenshot = "Z:\snapshots\s12_credits.jpg"

    intro_start = find_screenshot_time(in_filename, intro_screenshot, search_start_time=60, search_duration=300)
    intro_start_offset = -1
    intro_start = intro_start + intro_start_offset

    intro_length = 23.5
    intro_end = intro_start + intro_length

    credits_start = find_screenshot_time(in_filename, credits_screenshot, search_start_time=1000, search_duration=300)

    # calculate new end time for trimmed video. 
    credits_start_offset = 0.75
    end_duration = credits_start + credits_start_offset - intro_end

    """ clip videos: before intro; after intro but before credits.
    need to use ss and t parameters and not .trim(). .trim() doesn't clip out sound
    ss = start time
    t = clip duration (not clip timestamp) """
    i1 = ffmpeg.input(in_filename, ss=0.0, t=intro_start)
    i2 = ffmpeg.input(in_filename, ss=intro_end, t=end_duration)

    # get video and audio streams, join them, then write the final output.
    v1 = i1.video
    a1 = i1.audio
    v2 = i2.video
    a2 = i2.audio

    joined = ffmpeg.concat(v1, a1, v2, a2, v=1, a=1).node
    v3 = joined[0]
    a3 = joined[1]
    
    out = ffmpeg.output(v3, a3, out_filename)
    out.run()


''' Returns the timestamp in a video that matches a screenshot '''
def find_screenshot_time(in_filename, screenshot, search_start_time=0.0, search_duration=0.0):

    if (search_duration==0.0):
        # get total time in video    
        probe = ffmpeg.probe(in_filename)
        search_duration = float(probe['format']['duration'])

    """ find all matching frames for the screenshot.
        -ss = start time
        -t = search time 
        blackframe = amount of pixels matching the screenshot in each frame e.g. 99:32. 99% of pixels are less than
        returns a large string of information."""
    subprocess_result = subprocess.getoutput("ffmpeg.exe -ss %d -t %d -i \"%s\" -loop 1 -i \"%s\" -an -filter_complex \"[0]extractplanes=y[v];[1]extractplanes=y[i];[v][i]blend=difference:shortest=1,blackframe=99:32\" -f null -" % (search_start_time, search_duration, in_filename, screenshot))

    # find floating point number in string that is after " t:". e.g. " t:50.2424". This is the timestamp of the frames that match the image.
    # take the first one in case of multiple matches.
    screenshot_time = float(re.compile(' t:(\d+\.\d+)').findall(subprocess_result)[0]) + search_start_time

    return screenshot_time

if __name__ == "__main__":
    main()