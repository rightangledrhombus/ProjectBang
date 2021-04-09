import os
import subprocess
import ffmpeg
import re

def main():

    # Fina all .mp4 files in a directory.
    parent_dir = r"Z:\The Big Bang Theory S01-S10 (2007-)\season12_temp"
    #parent_dir = r"G:\Plex\The Big Bang Theory\The Big Bang Theory S01-S10 (2007-)\season12_temp"
    files_path = [os.path.join(r,file) for r,d,f in os.walk(parent_dir) for file in f if file.endswith(".mp4")]

    for in_filename in files_path:
        in_filename_split = os.path.splitext(in_filename)
        out_filename_clipped = in_filename_split[0] + "_trim" + in_filename_split[1]
        out_filename_color = in_filename_split[0] + "_color" + in_filename_split[1]
        
        remove_intro_and_credits(in_filename, out_filename_clipped)   
        #change_color_temperature(in_filename, out_filename_color, temperature=4000)   


def remove_intro_and_credits(in_filename, out_filename):
    
    intro_screenshot = r"Z:\snapshots\s12_intro.jpg"
    credits_screenshot = r"Z:\snapshots\s12_credits.jpg"

    # get all timestamps in the video that match the still frames of the intro and credits.
    intro_start = find_screenshot_time(in_filename, intro_screenshot, search_start_time=60, search_duration=300)
    intro_start_offset = -1
    intro_start = intro_start + intro_start_offset

    intro_length = 23.5
    intro_end = intro_start + intro_length

    credits_start = find_screenshot_time(in_filename, credits_screenshot, search_start_time=1000, search_duration=300)

    # calculate new end time for clipped video. 
    credits_start_offset = 0.75
    end_duration = credits_start + credits_start_offset - intro_end

    """ clip videos: before intro; after intro but before credits.
    need to use ss and t parameters and not .trim(). .trim() doesn't clip out sound
    ss = start time
    t = clip duration (not clip timestamp) """
    i1 = ffmpeg.input(in_filename, ss=0.0, t=intro_start)
    i2 = ffmpeg.input(in_filename, ss=intro_end, t=end_duration)

    concat_videos(i1, i2, out_filename)
    
""" Concat two video streams together """
def concat_videos(i1, i2, out_filename):
    # get video and audio streams, join them, then write the final output.
    v1 = i1.video
    a1 = i1.audio
    v2 = i2.video
    a2 = i2.audio

    joined = ffmpeg.concat(v1, a1, v2, a2, v=1, a=1).node
    v3 = joined[0]
    a3 = joined[1]
    
    out = ffmpeg.output(v3, a3, out_filename)
    return out.run(overwrite_output=True)


''' Returns the timestamp in a video that matches an image '''
def find_screenshot_time(in_filename, image_filename, search_start_time=0.0, search_duration=0.0):

    if (search_duration==0.0):
        # get total time in video    
        probe = ffmpeg.probe(in_filename)
        search_duration = float(probe['format']['duration'])

    """ find all matching frames for the screenshot.
        -ss = start time
        -t = search time 
        blackframe = amount of pixels matching the screenshot in each frame e.g. 99:32. 99% of pixels are less than 32 value in the
        difference image between the video frame and still image.
        returns a large string of information."""
    subprocess_result = subprocess.getoutput("ffmpeg.exe -ss %d -t %d -i \"%s\" -loop 1 -i \"%s\" -an -filter_complex \"[0]extractplanes=y[v];[1]extractplanes=y[i];[v][i]blend=difference:shortest=1,blackframe=99:32\" -f null -" % (search_start_time, search_duration, in_filename, image_filename))

    # find floating point number in string that is after " t:". e.g. " t:50.2424". This is the timestamp of the frames that match the image.
    # take the first one in case of multiple matches.
    screenshot_time = float(re.compile(r' t:(\d+\.\d+)').findall(subprocess_result)[0]) + search_start_time

    return screenshot_time

""" Changes the color temperature of a video. 
    temperature = temp in kelvin in incrememts of 500 from 1000-10000 """
def change_color_temperature(in_filename, out_filename, temperature):
    
    # table of values for different temperatures
    kelvin_table = {
    1000: (255,56,0),
    1500: (255,109,0),
    2000: (255,137,18),
    2500: (255,161,72),
    3000: (255,180,107),
    3500: (255,196,137),
    4000: (255,209,163),
    4500: (255,219,186),
    5000: (255,228,206),
    5500: (255,236,224),
    6000: (255,243,239),
    6500: (255,249,253),
    7000: (245,243,255),
    7500: (235,238,255),
    8000: (227,233,255),
    8500: (220,229,255),
    9000: (214,225,255),
    9500: (208,222,255),
    10000: (204,219,255)}

    if (temperature % 500):
        raise Exception("Temperature must be a multiple of 500 in the range 100-10000")

    r, g, b = kelvin_table[temperature]

    i1 = ffmpeg.input(in_filename)
    v1 = i1.video
    a1 = i1.audio

    v1_color = v1.colorchannelmixer(rr=r/255, gg=g/255, bb=b/255)

    # Need to force the pix_fmt to yuv420p for apps to play it. The colorchannel mixer tries to change it by default.
    out = ffmpeg.output(v1_color, a1, out_filename, pix_fmt='yuv420p')
    out.run(overwrite_output=True)

if __name__ == "__main__":
    main()