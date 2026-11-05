"""
Unit tests for TokenCompressor.
"""

import unittest
from agent_token_optimizer.compressor import TokenCompressor

class TestTokenCompressor(unittest.TestCase):
    def setUp(self):
        self.compressor = TokenCompressor()

    def test_strip_filler(self):
        text = "Certainly! Here is the information you requested: The server is healthy. I hope this helps!"
        compressed, stats = self.compressor.compress_text(text)
        self.assertNotIn("Certainly", compressed)
        self.assertNotIn("I hope this helps", compressed)
        self.assertIn("The server is healthy.", compressed)
        self.assertGreater(stats.char_reduction_pct, 40.0)

    def test_phrase_simplification(self):
        text = "In order to deploy the container due to the fact that config changed, please note that port is 8080."
        compressed, _ = self.compressor.compress_text(text)
        self.assertIn("to deploy", compressed)
        self.assertIn("because config changed", compressed)
        self.assertIn("note: port is 8080.", compressed)

    def test_whitespace_collapse(self):
        text = "Hello       world!\n\n\n\nNew line."
        compressed, _ = self.compressor.compress_text(text)
        self.assertEqual(compressed, "Hello world!\n\nNew line.")

if __name__ == "__main__":
    unittest.main()
