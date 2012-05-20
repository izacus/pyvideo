import unittest
from unittest.case import TestCase
import pyvideo

class DecodingPerformanceTests(TestCase):
    def setUp(self):
        pass

    def testFullDecode(self):
        source = pyvideo.load("test_media/test_video.mp4")
        timestamp = source.get_next_video_timestamp()
        self.assertIsNotNone(timestamp)

        while timestamp is not None:
            frame = source.get_next_video_frame()
            timestamp = source.get_next_video_timestamp()
            # Decode audio data until the next frame
            while True:
                audio_data = source.get_audio_data()
                if audio_data is None or audio_data.timestamp > timestamp:
                    break

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()