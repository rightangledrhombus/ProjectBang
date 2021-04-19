import unittest
import os
from pathlib import Path
import video_manipulator

class TestVideos(unittest.TestCase):

    def test_find_screenshot_time(self):
        in_filename = in_filename = r"Z:\unittest\The.Big.Bang.Theory.S12E09.WEBRip.x264-ION10.mp4"
        screenshot = screenshot = r"Z:\unittest\s12_intro.jpg"
        search_start_time = 250
        search_duration = 90
        time = video_manipulator.find_screenshot_time(in_filename, screenshot, search_start_time=search_start_time, search_duration=search_duration)
        
        self.assertEqual(time, 250.541956)

    def test_video_container_convert(self):
        in_filename_path = r"Z:\unittest\short_video"
        in_filename = in_filename_path + ".mp4"
        out_container = "mkv"        
        
        video_manipulator.convert_video_container(in_filename, out_container)
        
        out_filename = in_filename_path + ".mkv"
        path = Path(out_filename)
        self.assertTrue((str(path), path.is_file()), (str(path), True))

if __name__ == '__main__':
    unittest.main()
