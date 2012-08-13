import unittest

from taskcardmaker.model import Settings
from taskcardmaker.parser import TaskCardParser, ParsingError

class TaskCardParserTest (unittest.TestCase):
    def setUp (self):
        self.parser = TaskCardParser()

    def test_should_raise_parsing_error_when_using_setting_colorswith_unknown_value (self):
        self.assertRaises(ParsingError, self.parser.parse, "# colors caboom")

    def test_should_parse_setting_colors_with_foreground(self):
        self.parser.parse("# colors foreground")
        self.assertEquals(Settings.COLORS_FOREGROUND, self.parser.settings.colors)

    def test_should_parse_setting_colors_with_value_background (self):
        self.parser.parse("# colors background")
        self.assertEquals(Settings.COLORS_BACKGROUND, self.parser.settings.colors)

    def test_should_raise_parsing_error_when_using_setting_storycards_with_unknown_value (self):
        self.assertRaises(ParsingError, self.parser.parse, "# storycards caboom")

    def test_should_parse_setting_storycards_with_value_no (self):
        self.parser.parse("# storycards no")
        self.assertFalse(self.parser.settings.render_storycards)

    def test_should_parse_setting_storycards_with_value_yes (self):
        self.parser.parse("# storycards yes")
        self.assertTrue(self.parser.settings.render_storycards)

    def test_should_raise_syntax_error_when_unknown_settings_is_used  (self):
        self.assertRaises(ParsingError, self.parser.parse, "# spam eggs")

    def test_should_raise_syntax_error_when_width_setting_has_error  (self):
        self.assertRaises(ParsingError, self.parser.parse, "# width caboom")
        
    def test_should_parse_width_setting (self):
        self.parser.parse("# width 70")
        self.assertEquals(70, self.parser.settings.card_width)

    def test_should_raise_syntax_error_when_font_size_setting_has_error  (self):
        self.assertRaises(ParsingError, self.parser.parse, "# font_size caboom")
        
    def test_should_parse_font_size_setting (self):
        self.parser.parse("# font_size 13")
        self.assertEquals(13, self.parser.settings.font_size)

    def test_should_parse_multiple_settings (self):
        self.parser.parse("# font_size 13", "#width 13")
        
    def test_should_raise_exception_when_parsing_checkbox_setting_with_invalid_value (self):
        self.assertRaises(ParsingError, self.parser.parse, "# checkboxes spam")

    def test_should_disable_checkboxes_when_parsing_checkbox_setting (self):
        self.parser.parse("# checkboxes no")
        self.assertFalse(self.parser.settings.render_check_box)
        
    def test_should_raise_exception_when_parsing_qrcode_setting_with_invalid_value (self):
        self.assertRaises(ParsingError, self.parser.parse, "# qrcodes spam")

    def test_should_enable_qrcodes_when_parsing_qrcodes_setting (self):
        self.parser.parse("# qrcodes yes")
        self.assertTrue(self.parser.settings.render_qrcode)

    def test_should_raise_syntax_error_when_story_line_has_syntax_error (self):
        self.assertRaises(ParsingError, self.parser.parse, "S:")

    def test_should_parse_story_when_only_id_is_given (self):
        self.parser.parse("S:SPAM")

        project = self.parser.project
        self.assertEquals(1, len(project.stories))
        
        story = project.stories[0]
        self.assertEquals("SPAM", story.identifier)
        self.assertEquals(["SPAM"], story.title)        
        
    def test_should_parse_single_task (self):
        self.parser.parse("P:I18N", "S:IP-275|Sortierung nach Aktualitaet",
                          "Beispieltask")
        project = self.parser.project
        
        self.assertEquals("I18N", project.name)
        self.assertEquals(1, len(project.stories))
        
        story = project.stories[0]
        self.assertEquals("IP-275", story.identifier)
        self.assertEquals(["Sortierung nach Aktualitaet"], story.title)
        self.assertEquals(1, len(story.tasks))
        
        task = story.tasks[0]
        self.assertEquals(["Beispieltask"], task.description)

    def test_should_parse_single_task_without_project (self):
        self.parser.parse("S:IP-275|Sortierung nach Aktualitaet",
                          "Beispieltask")
        project = self.parser.project
        
        self.assertEquals("", project.name)
        self.assertEquals(1, len(project.stories))
        
        story = project.stories[0]
        self.assertEquals("IP-275", story.identifier)
        self.assertEquals(["Sortierung nach Aktualitaet"], story.title)
        self.assertEquals(1, len(story.tasks))
        
        task = story.tasks[0]
        self.assertEquals(["Beispieltask"], task.description)

    def test_should_parse_single_task_with_single_tag (self):
        self.parser.parse("P:I18N", "S:IP-275|Sortierung nach Aktualitaet",
                          "Beispieltask|TAG")
        
        task = self.parser.project.stories[0].tasks[0]
        self.assertEquals(["TAG"], task.tags)

    def test_should_parse_single_task_with_multiple_tags (self):
        self.parser.parse("P:I18N", "S:IP-275|Sortierung nach Aktualitaet",
                          "Beispieltask|TAG,TAG2")
        
        task = self.parser.project.stories[0].tasks[0]
        self.assertEquals(["TAG", "TAG2"], task.tags)

    def test_should_strip_whitespace_in_project (self):
        self.parser.parse("P:  I18N               ",)
        
        self.assertEquals("I18N", self.parser.project.name)

    def test_should_strip_whitespace_in_story_identifier_and_title (self):
        self.parser.parse("S:  IP-275          |     Lorem ipsum             ")
        
        self.assertEquals("IP-275", self.parser.project.stories[0].identifier)
        self.assertEquals(["Lorem ipsum"], self.parser.project.stories[0].title)

    def test_should_strip_whitespace_in_task_text_and_tags (self):
        self.parser.parse("S:IP-275|Lorem ipsum", "      Foo    |    Bar    , Foo ")
        
        self.assertEquals(["Foo"],
                          self.parser.project.stories[0].tasks[0].description)
        self.assertEquals(["Bar", "Foo"],
                          self.parser.project.stories[0].tasks[0].tags)

    def test_should_parse_blocker_tasks (self):
        self.parser.parse("S:IP-275|", "Foo|BLOCKER", "Bar")
        
        self.assertTrue(self.parser.project.stories[0].tasks[0].blocker)
        self.assertFalse(self.parser.project.stories[0].tasks[1].blocker)

    def test_should_parse_task_with_multiline_description (self):
        self.parser.parse("S:IP-275|", "Spam\\and\\Eggs")
        
        self.assertEquals(["Spam", "and", "Eggs"], 
                          self.parser.project.stories[0].tasks[0].description)

    def test_should_parse_story_with_multiline_description (self):
        self.parser.parse("S:IP-275|Spam\\and\\Eggs")
        
        self.assertEquals(["Spam", "and", "Eggs"], 
                          self.parser.project.stories[0].title)
