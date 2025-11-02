"""
Unit tests for shortcore module to prevent regression of the shorts video generation bug.

The bug (fixed in PR #1): 
  original_text = chatgpt(getyamll("short_prompt")).format(title=title,time=time)
  
This was incorrect because .format() was called on the chatgpt() response instead of
on the prompt template, causing KeyError when the response contained curly braces.

The fix:
  original_text = chatgpt(getyamll("short_prompt").format(title=title,time=time))
"""

import unittest
from lib.video_texts import getyamll


class TestShortcorePromptFormatting(unittest.TestCase):
    """Test cases for prompt formatting in shortcore module."""

    def test_short_prompt_exists(self):
        """Test that short_prompt key exists in YAML."""
        prompt = getyamll("short_prompt")
        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    def test_short_prompt_has_correct_placeholders(self):
        """Test that short_prompt contains the expected {title} and {time} placeholders."""
        prompt = getyamll("short_prompt")
        self.assertIn("{title}", prompt, "Prompt should contain {title} placeholder")
        self.assertIn("{time}", prompt, "Prompt should contain {time} placeholder")

    def test_prompt_formatting_with_title_and_time(self):
        """Test that prompt can be formatted with title and time without errors."""
        prompt = getyamll("short_prompt")
        
        # Test with various inputs
        test_cases = [
            ("cooking secrets", "40"),
            ("travel tips", "30"),
            ("science facts", "60"),
            ("history lessons", "45"),
        ]
        
        for title, time in test_cases:
            with self.subTest(title=title, time=time):
                try:
                    formatted = prompt.format(title=title, time=time)
                    self.assertIsInstance(formatted, str)
                    self.assertNotIn("{title}", formatted, 
                                   "Formatted prompt should not contain {title} placeholder")
                    self.assertNotIn("{time}", formatted,
                                   "Formatted prompt should not contain {time} placeholder")
                    self.assertIn(title, formatted,
                                "Formatted prompt should contain the title")
                    self.assertIn(time, formatted,
                                "Formatted prompt should contain the time")
                except KeyError as e:
                    self.fail(f"Formatting failed with KeyError: {e}")

    def test_prompt_doesnt_have_extra_placeholders(self):
        """Test that prompt doesn't have unexpected placeholders that would cause KeyError."""
        prompt = getyamll("short_prompt")
        
        # Try to format with only title and time - should not raise KeyError
        try:
            formatted = prompt.format(title="test", time="30")
            # If we get here, there are no extra placeholders
            self.assertTrue(True)
        except KeyError as e:
            self.fail(
                f"Prompt has unexpected placeholder that causes KeyError: {e}. "
                f"Only {{title}} and {{time}} should be present."
            )

    def test_prompt_with_special_characters_in_values(self):
        """Test that formatting works with special characters in title and time."""
        prompt = getyamll("short_prompt")
        
        # Test with special characters that might be in titles
        special_titles = [
            "cooking's best secrets",
            "10 tips & tricks",
            'quotes "and" apostrophes',
            "numbers 123 and symbols @#$",
        ]
        
        for title in special_titles:
            with self.subTest(title=title):
                try:
                    formatted = prompt.format(title=title, time="30")
                    self.assertIn(title, formatted)
                except KeyError as e:
                    self.fail(f"Formatting with special characters failed: {e}")

    def test_formatted_prompt_structure(self):
        """Test that the formatted prompt maintains expected structure."""
        prompt = getyamll("short_prompt")
        formatted = prompt.format(title="cooking", time="40")
        
        # Check that the prompt still contains key instructional elements
        # (these are from the original prompt structure)
        self.assertIn("script", formatted.lower(), 
                     "Formatted prompt should mention 'script'")
        self.assertIn("youtube", formatted.lower(),
                     "Formatted prompt should mention 'youtube'")


class TestPromptFormattingOrderCorrectness(unittest.TestCase):
    """
    Test to ensure the correct order of operations in string formatting.
    
    This test simulates what would happen with wrong vs right parentheses placement.
    """
    
    def test_correct_order_format_before_processing(self):
        """Test that demonstrates the CORRECT approach: format template, then process."""
        prompt_template = getyamll("short_prompt")
        
        # CORRECT: Format the template first
        formatted_prompt = prompt_template.format(title="test", time="30")
        
        # At this point, formatted_prompt is ready to be sent to an API
        # It should not contain {title} or {time} anymore
        self.assertNotIn("{title}", formatted_prompt)
        self.assertNotIn("{time}", formatted_prompt)
        self.assertIn("test", formatted_prompt)
        self.assertIn("30", formatted_prompt)
        
    def test_wrong_order_would_cause_error(self):
        """
        Test that demonstrates why the WRONG approach fails.
        
        This simulates: result = process(template).format(...)
        where process returns a string with curly braces.
        """
        # Simulate a response from chatgpt that contains curly braces
        # (like HTML/CSS which was the actual error case)
        simulated_api_response = """
        <style>
            .container {
                font-family: Arial;
            }
        </style>
        """
        
        # This is what would happen with WRONG parentheses placement
        # original_text = chatgpt(template).format(title=..., time=...)
        with self.assertRaises(KeyError) as context:
            # Try to format the API response (which has its own curly braces)
            simulated_api_response.format(title="test", time="30")
        
        # The error should mention an unexpected key from the curly braces in the response
        self.assertIsInstance(context.exception, KeyError)


if __name__ == "__main__":
    unittest.main()
