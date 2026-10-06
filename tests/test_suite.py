import unittest
from tamilai.transliterate import transliterate_text
from tamilai.analyzer import analyze_text
from tamilai.prompt import build_prompt

class TestTamilAISuite(unittest.TestCase):

    def test_transliterate_common_words(self):
        output = transliterate_text("vanakkam nanba eppadi irukkiraai")
        self.assertIn("வணக்கம்", output)
        self.assertIn("நண்பா", output)
        self.assertIn("எப்படி", output)
        self.assertIn("இருக்கிறாய்", output)

    def test_analyze_text(self):
        result = analyze_text("தமிழ் மொழி மிகவும் பழமையான மற்றும் அருமையான மொழி!")
        self.assertGreater(result["tamil_character_count"], 30)
        self.assertGreater(result["tamil_ratio_percent"], 50.0)
        self.assertEqual(result["sentiment"], "Positive (நேர்மறை)")

    def test_build_prompt(self):
        prompt = build_prompt("translate_en_ta", "Hello world")
        self.assertIn("Hello world", prompt)
        self.assertIn("Tamil Translation:", prompt)

if __name__ == "__main__":
    unittest.main()
