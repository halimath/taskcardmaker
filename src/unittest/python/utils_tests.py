import unittest
from pyassert import *

from taskcardmaker.utils import CamelCaseHyphenator

class CamelCaseHyphenatorTest (unittest.TestCase):
    def setUp (self):
        self.hyphenator = CamelCaseHyphenator()

    def test_should_return_list_with_empty_string_when_word_is_empty (self):
        assert_that(self.hyphenator.hyphenate('')).equals([''])

    def test_should_return_single_syliable_when_word_contains_no_upper_case_letters (self):
        assert_that(self.hyphenator.hyphenate('spam')).equals(['spam'])

    def test_should_return_two_syliable_when_word_contains_single_upper_case_letters (self):
        assert_that(self.hyphenator.hyphenate('spamEggs')).equals(['spam', 'Eggs'])

    def test_should_return_two_syliable_when_word_contains_single_upper_case_letters_and_starts_with_uppercase_letter (self):
        assert_that(self.hyphenator.hyphenate('SpamEggs')).equals(['Spam', 'Eggs'])
