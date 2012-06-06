import unittest
from unittest.case import TestCase
import pyvideo

class DecodingComplianceTests(TestCase):
    def setUp(self):
        pass
    
    def testMetaData(self):
        source = pyvideo.load("test_media/test_video.mp4")
        self.assertAlmostEqual(source.duration, 10.041667)
        video_format = source.video_format
        self.assertEqual(video_format.height, 480)
        self.assertEqual(video_format.width, 854)
        audio_format = source.audio_format
        self.assertEqual(audio_format.channels, 2)
        self.assertEqual(audio_format.sample_size, 16)
        self.assertEqual(audio_format.sample_rate, 48000)

    def testFullDecode(self):
        source = pyvideo.load("test_media/victoria.webm")
        self.assertIsNotNone(source.audio_format)
        self.assertIsNotNone(source.video_format)

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
