import unittest

from batch.spiders.pc_part_picker import _parse_chrome_major_version


class ChromeVersionParsingTests(unittest.TestCase):
    def test_parses_google_chrome_version(self):
        self.assertEqual(_parse_chrome_major_version("Google Chrome 155.0.8059.85"), 155)

    def test_parses_chromium_version(self):
        self.assertEqual(_parse_chrome_major_version("Chromium 156.0.1"), 156)

    def test_unknown_output_returns_none(self):
        self.assertIsNone(_parse_chrome_major_version("Just a moment..."))


if __name__ == "__main__":
    unittest.main()
