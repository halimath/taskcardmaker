import unittest

from taskcardmaker.parser import TaskCardParser

class TaskCardParserTest (unittest.TestCase):
    def setUp (self):
        self.parser = TaskCardParser()
        
    def test_should_parse_single_task (self):
        self.parser.parse("P:I18N", "S:IP-275|Sortierung nach Aktualitaet",
                          "Beispieltask")
        project = self.parser.project
        
        self.assertEquals("I18N", project.name)
        self.assertEquals(1, len(project.stories))
        
        story = project.stories[0]
        self.assertEquals("IP-275", story.identifier)
        self.assertEquals("Sortierung nach Aktualitaet", story.title)
        self.assertEquals(1, len(story.tasks))
        
        task = story.tasks[0]
        self.assertEquals("Beispieltask", task.description)

    def test_should_parse_single_task_without_project (self):
        self.parser.parse("S:IP-275|Sortierung nach Aktualitaet",
                          "Beispieltask")
        project = self.parser.project
        
        self.assertEquals("", project.name)
        self.assertEquals(1, len(project.stories))
        
        story = project.stories[0]
        self.assertEquals("IP-275", story.identifier)
        self.assertEquals("Sortierung nach Aktualitaet", story.title)
        self.assertEquals(1, len(story.tasks))
        
        task = story.tasks[0]
        self.assertEquals("Beispieltask", task.description)

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
        self.assertEquals("Lorem ipsum", self.parser.project.stories[0].title)

    def test_should_strip_whitespace_in_task_text_and_tags (self):
        self.parser.parse("S:IP-275|Lorem ipsum", "      Foo    |    Bar    , Foo ")
        
        self.assertEquals("Foo",
                          self.parser.project.stories[0].tasks[0].description)
        self.assertEquals(["Bar", "Foo"],
                          self.parser.project.stories[0].tasks[0].tags)

    def test_should_parse_blocker_tasks (self):
        self.parser.parse("S:IP-275|", "B:Foo", "Bar")
        
        self.assertTrue(self.parser.project.stories[0].tasks[0].blocker)
        self.assertFalse(self.parser.project.stories[0].tasks[1].blocker)

