import unittest
import os
from pathlib import Path
import bang_convert

class TestVideos(unittest.TestCase):

    def test_find_screenshot_time(self):
        in_filename = in_filename = "Z:\The Big Bang Theory S01-S10 (2007-)\The Big Bang Theory S02 (360p re-blurip)\The Big Bang Theory S02E01 The Bad Fish Paradigm.mp4"
        screenshot = screenshot = "Z:\snapshots\s02e01_intro.jpg"
        search_start_time = 200
        search_duration = 100
        time = bang_convert.find_screenshot_time(in_filename, screenshot, search_start_time=search_start_time, search_duration=search_duration)
        self.assertEqual(time, 50.541956)

if __name__ == '__main__':
    unittest.main()
