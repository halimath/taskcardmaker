import taskcardmaker

from taskcardmaker.canvas import Canvas, Point
from taskcardmaker.model import Settings
from taskcardmaker.utils import CamelCaseHyphenator

WHITE = (1, 1, 1)
BLACK = (0, 0, 0)

STORY_BACKGROUND = (.5, .8, 1)
STORY_FOREGROUND = (.2, .4, .5)

BLOCKER_TASK_BACKGROUND = (1, .5, .5)
BLOCKER_TASK_FOREGROUND = (.5, .2, .2)

NORMAL_TASK_BACKGROUND = (1, 1, .5)
NORMAL_TASK_FOREGROUND = (.5, .5, .2)

class Renderer (object):
    PAPER_WIDTH = 210
    INITIAL_X = 15
    MAX_LINES_IN_BOX_DESCRIPTION = 5
    BOX_OUTER_LINES_THICKNESS = 1
    BOX_INNER_LINES_THICKNESS = .2

    def __init__ (self, filename_or_file_like_object, title=None, author=None):
        self.hyphenator = CamelCaseHyphenator()

        self.current_point = Point(Renderer.INITIAL_X, 287)
        self.card_written = False
        self.canvas = Canvas(filename_or_file_like_object, title, author)
        self.stories_written = 0

        self.settings = Settings()

    def __enter__ (self):
        return self

    def __exit__ (self, exception_type, exception_value, traceback):
        self.close()

    def close (self):
        self.canvas.close()

    def apply_settings (self, settings):
        self.settings = settings

    def render_story (self, story):
        if self.settings.render_storycards:
            self.move_to_next_box()

            self.render_story_box()
            self.render_story_box_lines()

            self.select_story_font_color()

            self.render_story_identifier(story)
            self.render_story_title(story)

        for task in story.tasks:
            self.render_task(task)

    def render_task (self, task):
        self.move_to_next_box()

        self.render_task_box(task)
        self.render_task_box_lines()

        self.select_task_font_color(task)

        self.canvas.select_font(size=self.settings.font_size * 1.1, family="Helvetica-Bold")
        self.render_task_title(task)

        self.canvas.select_font(size=self.settings.font_size, family="Helvetica")
        self.render_task_description(task)
        self.render_task_tags(task)

    def move_to_next_box (self):
        if not self.card_written:
            self.write_footer()
            self.card_written = True
            return

        if self.current_point.x + 2 * self.settings.card_width > Renderer.PAPER_WIDTH:
            self.current_point = self.current_point.move(y= -self.settings.card_width)
            self.current_point.x = Renderer.INITIAL_X
        else:
            self.current_point = self.current_point.move(x=self.settings.card_width)

        if self.current_point.y - self.settings.card_width < 10:
            self.next_page()

    def next_page (self):
        self.canvas.next_page()
        self.current_point = Point(Renderer.INITIAL_X, 287)
        self.write_footer()

    def write_footer (self):
        self.canvas.fill_color((0, 0, 0))
        self.canvas.select_font(size=8, family="Helvetica")
        footer = "Made with Taskcardmaker %s - http://taskcardmaker.appspot.com - https://github.com/halimath/taskcardmaker" % taskcardmaker.version
        width = self.canvas.text_width(footer)
        self.canvas.text(Point((Renderer.PAPER_WIDTH - width) / 2, 5), footer)

    def render_story_identifier (self, story):
        self.canvas.select_font(size=self.settings.font_size * 5, family="Helvetica-Bold")
        identifier = self.abbreviate_to_width(story.identifier)
        width = self.canvas.text_width(identifier)

        self.canvas.text(self.current_point.move(x=(self.settings.card_width - width) / 2,
                                                 y= -25),
                         identifier)

    def render_story_title (self, story):
        self.canvas.select_font(size=self.settings.font_size * 1.2, family="Helvetica-Bold")

        width = self.settings.card_width - 10
        lines = self.break_into_lines(story.title, width)

        i = 0
        for line in lines[0:3]:
            self.canvas.text(self.current_point.move(x=5,
                                                     y= -40 - 6 * i),
                             line)
            i += 1

    def render_story_box(self):
        foreground = BLACK
        background = STORY_BACKGROUND

        if self.settings.colors == Settings.COLORS_FOREGROUND:
            foreground = STORY_FOREGROUND
            background = WHITE

        self.render_box(background, foreground)


    def render_task_box(self, task):
        foreground = BLACK
        background = BLOCKER_TASK_BACKGROUND if task.blocker else NORMAL_TASK_BACKGROUND

        if self.settings.colors == Settings.COLORS_FOREGROUND:
            foreground = BLOCKER_TASK_FOREGROUND if task.blocker else NORMAL_TASK_FOREGROUND
            background = WHITE

        self.render_box(background, foreground)

    def render_task_tags (self, task):
        self.canvas.select_font(size=self.settings.font_size * .9, family="Helvetica-Bold")
        tags_string = " | ".join(task.tags)
        width = self.settings.card_width - 4
        if self.settings.render_check_box:
            width -= self.calculate_check_box_width() + 6
        tags_string = self.abbreviate_to_width(tags_string, max_width=width - 1)
        text_width = self.canvas.text_width(tags_string)

        self.canvas.text(self.current_point.move(x=(width - text_width) / 2,
                                                 y= -self.settings.card_width + 6),
                         tags_string)

    def render_task_title (self, task):
        title = self.abbreviate_to_width(task.story.identifier,
                                         max_width=self.settings.card_width - 4)
        width = self.canvas.text_width(title)

        self.canvas.text(self.current_point.move(x=(self.settings.card_width - width) / 2,
                                                 y= -10), title)

    def render_task_description(self, task):
        lines = self.break_into_lines(task.description,
                                      max_width=self.settings.card_width - 15)
        line_number = 1
        if len(lines) > Renderer.MAX_LINES_IN_BOX_DESCRIPTION:
            lines = lines[:Renderer.MAX_LINES_IN_BOX_DESCRIPTION - 1] + ["..."]
        for line in lines:
            self.canvas.text(self.current_point.move(x=3,
                                                     y= -12 - 6 * line_number),
                             line)
            line_number += 1

    def abbreviate_to_width (self, text, max_width=None):
        if not max_width:
            max_width = self.settings.card_width - 2

        if self.canvas.text_width(text) <= max_width:
            return text

        abbreviated = ""

        for c in text:
            if self.canvas.text_width(abbreviated + c + "...") > max_width:
                return abbreviated + "..."
            else:
                abbreviated += c

        return abbreviated + "..."

    def break_into_lines (self, lines, max_width=None):
        if not max_width:
            max_width = self.settings.card_width

        result = []

        for line in lines:
            words = line.split()
            current_line = []

            while words:
                word = words[0]
                current_line_as_string = " ".join(current_line)

                if self.canvas.text_width(" ".join(current_line + [word])) > max_width:
                    # try to hyphenate
                    syliables = self.hyphenator.hyphenate(word)
                    for i in range(1, len(syliables)):
                        candidate = current_line_as_string + " " + "".join(syliables[0:i]) + "-"
                        if self.canvas.text_width(candidate) > max_width:
                            if i > 0:
                                words.pop(0)
                                current_line.append("".join(syliables[0:i]) + "-")
                                result.append(" ".join(current_line))
                                words.insert(0, "".join(syliables[i:-1]))
                            break

                    current_line = []
                else:
                    current_line.append(word)
                    words.pop(0)

            result.append(" ".join(current_line))

        return result

    def render_box (self, background_color, foreground_color=(0, 0, 0)):
        self.canvas.line_width(Renderer.BOX_OUTER_LINES_THICKNESS)
        self.canvas.fill_color(background_color)

        self.canvas.text_color(foreground_color)
        self.canvas.draw_rect(self.current_point, self.settings.card_width - 1)

    def render_task_box_lines (self):
        self.canvas.line_width(Renderer.BOX_INNER_LINES_THICKNESS)
        self.canvas.line(self.current_point.move(x=4, y= -12),
                         self.current_point.move(x=self.settings.card_width - 4, y= -12))

        self.canvas.line(self.current_point.move(x=4,
                                                 y= -self.settings.card_width + 15),
                         self.current_point.move(x=self.settings.card_width - 4,
                                                 y= -self.settings.card_width + 15))

        if self.settings.render_check_box:
            check_box_width = self.calculate_check_box_width()
            self.canvas.draw_rect(self.current_point.move(x=self.settings.card_width - check_box_width - 4,
                                                          y= -self.settings.card_width + 11),
                                  width=check_box_width, fill=False)

    def calculate_check_box_width (self):
        return self.settings.card_width / 10

    def render_story_box_lines (self):
        self.canvas.line_width(Renderer.BOX_INNER_LINES_THICKNESS)
        delta = 30
        self.canvas.line(self.current_point.move(x=4, y= -delta),
                         self.current_point.move(x=self.settings.card_width - 4,
                                                 y= -delta))
        
    def select_task_font_color (self, task):
        if self.settings.colors == Settings.COLORS_BACKGROUND:
            self.canvas.fill_color(BLACK)
        else:
            self.canvas.fill_color(BLOCKER_TASK_FOREGROUND if task.blocker else NORMAL_TASK_FOREGROUND)

        
    def select_story_font_color (self):
        if self.settings.colors == Settings.COLORS_BACKGROUND:
            self.canvas.fill_color(BLACK)
        else:
            self.canvas.fill_color(STORY_FOREGROUND)

