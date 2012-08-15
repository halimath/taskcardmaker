import unittest

from taskcardmaker.utils import CamelCaseHyphenator

class CamelCaseHyphenatorTest (unittest.TestCase):
    def setUp (self):
        self.hyphenator = CamelCaseHyphenator()

    def test_should_return_single_syliable_when_word_contains_no_upper_case_letters (self):
        self.assertEquals(['spam'], self.hyphenator.hyphenate('spam'))

    def test_should_return_two_syliable_when_word_contains_single_upper_case_letters (self):
        self.assertEquals(['spam', 'Eggs'], self.hyphenator.hyphenate('spamEggs'))

    def test_should_return_two_syliable_when_word_contains_single_upper_case_letters_and_starts_with_uppercase_letter (self):
        self.assertEquals(['Spam', 'Eggs'], self.hyphenator.hyphenate('SpamEggs'))