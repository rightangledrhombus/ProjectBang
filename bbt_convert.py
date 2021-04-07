import os
import subprocess
import ffmpeg
import json

def main():


    credits_time = 31.0
    in_filename = "Z:\The Big Bang Theory S01-S10 (2007-)\The Big Bang Theory S01 (360p re-blurip)\The Big Bang Theory S01E01 Pilot.mp4"
    in_filename_split = os.path.splitext(in_filename)
    out_filename = in_filename_split[0] + "_trim" + in_filename_split[1]
    
    # get total time in video
    #duration = subprocess.check_output("ffprobe.exe -i " + input_file + " -show_entries format=duration -v quiet -of csv=\"p=0\"") #segagesimal makes time hh:mm:ss format
    
    probe = ffmpeg.probe(in_filename)
    duration = float(probe['format']['duration'])

    # calculate new end time for trimmed video
    end_time = duration - credits_time

    input = ffmpeg.input(in_filename) \
                .trim(start=0.0, end=end_time) \
                .output(out_filename) \
                .run()
   
    # clip out credits and create trimmed video
    #subprocess.check_output("ffmpeg.exe -i %s -ss 00 -to %s %s" % (input_file, end_time, out_file))

if __name__ == "__main__":
    main()