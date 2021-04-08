import unittest
import os
from pathlib import Path
import bang_convert

class TestVideos(unittest.TestCase):

    def test_find_screenshot_time(self):
        in_filename = in_filename = "Z:\The Big Bang Theory S01-S10 (2007-)\season12_temp\The.Big.Bang.Theory.S12E09.WEBRip.x264-ION10.mp4"
        screenshot = screenshot = "Z:\snapshots\s12_intro.jpg"
        search_start_time = 250
        search_duration = 90
        time = bang_convert.find_screenshot_time(in_filename, screenshot, search_start_time=search_start_time, search_duration=search_duration)
        self.assertEqual(time, 250.541956)

if __name__ == '__main__':
    unittest.main()
