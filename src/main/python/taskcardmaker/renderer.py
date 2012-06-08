from taskcardmaker.canvas import Canvas, Point

class Renderer (object):
    PAPER_WIDTH = 210
    INITIAL_X = 15
    MAX_LINES_IN_BOX_DESCRIPTION = 5
    
    def __init__ (self, filenameOrFilelikeObject, title=None, author=None):
        self.current_point = Point(Renderer.INITIAL_X, 287)
        self.canvas = Canvas(filenameOrFilelikeObject, title, author)
        self.stories_written = 0
        self.box_width = 80
        self.font_size = 15
        
    def __enter__ (self):
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def close (self):
        self.canvas.close()
        
    def apply_settings (self, settings):
        self.box_width = settings.card_width
        self.font_size = settings.font_size
        
    def render_story (self, story):
        self._render_box((.5, .8, 1))
        self._render_story_box_lines()
        
        self._render_story_identifier(story)
        self._render_story_title(story)

        self._move_to_next_box()
              
        for task in story.tasks:
            self.render_task(task)        
        
    def render_task (self, task):
        self._render_box((1, .5, .5) if task.blocker else (1, 1, .5))
        self._render_task_box_lines()
        self._render_task_title(task)
        
        self.canvas.select_font(size=self.font_size, family="Helvetica")
        self._render_task_description(task)
        self._render_task_tags(task)
        
        self._move_to_next_box()

    def _move_to_next_box (self):
        if self.current_point.x + 2 * self.box_width > Renderer.PAPER_WIDTH:
            self.current_point = self.current_point.move(y=-self.box_width)
            self.current_point.x = Renderer.INITIAL_X
        else:
            self.current_point = self.current_point.move(x=self.box_width)
            
        if self.current_point.y - self.box_width < 10:
            self._next_page()        
        
    def _next_page (self):
        self.canvas.next_page()
        self.current_point = Point(Renderer.INITIAL_X, 287)
            
    def _render_story_identifier (self, story):
        self.canvas.fill_color((0, 0, 0))
        self.canvas.select_font(size=self.font_size * 5, family="Helvetica-Bold")
        identifier = self._abbreviate_to_width(story.identifier)
        width = self.canvas.text_width(identifier)
        
        self.canvas.text(self.current_point.move(x=(self.box_width - width) / 2, 
                                                 y=-25),
                         identifier)

    def _render_story_title (self, story):
        self.canvas.select_font(size=self.font_size * 1.2, family="Helvetica-Bold")
        lines = self._break_into_lines(story.title, self.box_width - 10)
        
        i = 0
        for line in lines[0:3]:
            self.canvas.text(self.current_point.move(x=5,
                                                     y=-40 - 7 * i), 
                             line)
            i += 1
            
    def _render_task_tags (self, task):
        self.canvas.fill_color((.4, .4, .4))
        self.canvas.select_font(size=self.font_size * 1.1, family="Helvetica-Bold")
        tags_string = " | ".join(task.tags)
        tags_string = self._abbreviate_to_width(tags_string)
        width = self.canvas.text_width(tags_string)
        
        self.canvas.text(self.current_point.move(x=(self.box_width - width) / 2, 
                                                 y=-self.box_width + 6),
                         tags_string)
            
    def _render_task_title (self, task):
        self.canvas.fill_color((0, 0, 0))
        self.canvas.select_font(size=self.font_size * 1.1, family="Helvetica-Bold")
        title = self._abbreviate_to_width(task.story.identifier, 
                                         max_width=self.box_width - 4)
        width = self.canvas.text_width(title)
        
        self.canvas.text(self.current_point.move(x=(self.box_width - width) / 2,
                                                 y=-10), title)
        
    def _render_task_description(self, task):
        lines = self._break_into_lines(task.description, 
                                      max_width=self.box_width - 10)
        line_number = 1
        if len(lines) > Renderer.MAX_LINES_IN_BOX_DESCRIPTION:
            lines = lines[:Renderer.MAX_LINES_IN_BOX_DESCRIPTION - 1] + ["..."]
        for line in lines:
            self.canvas.text(self.current_point.move(x=5, 
                                                     y=-12 + -6 * line_number), 
                             line)
            line_number += 1
            
    def _abbreviate_to_width (self, text, max_width=None):
        if not max_width:
            max_width = self.box_width
            
        if self.canvas.text_width(text) <= max_width:
            return text
        
        abbreviated = ""
        
        for c in text:
            if self.canvas.text_width(abbreviated + c + "...") > max_width:
                return abbreviated + "..."
            else:
                abbreviated += c
        
        return abbreviated + "..." 
        
    def _break_into_lines (self, text, max_width=None):
        if not max_width:
            max_width = self.box_width

        result = []
        
        words = text.split()
        current_line = []
        
        for word in words:
            if self.canvas.text_width(" ".join(current_line + [word])) > max_width:
                result.append(" ".join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        
        result.append(" ".join(current_line))
        
        return result            

    def _render_box (self, background_color):
        self.canvas.text_color((0, 0, 0))
        self.canvas.fill_color(background_color)
        self.canvas.fill_rect(self.current_point, self.box_width)


    def _render_task_box_lines (self):        
        self.canvas.line(self.current_point.move(x=4, y=-12), 
                         self.current_point.move(x=self.box_width - 4, y=-12))
        
        self.canvas.fill_color((.4, .4, .4))
        
        self.canvas.line(self.current_point.move(x=4, 
                                                 y=-self.box_width + 15), 
                         self.current_point.move(x=self.box_width - 4, 
                                                 y=-self.box_width + 15))

    def _render_story_box_lines (self):
        delta = 30
        self.canvas.line(self.current_point.move(x=4, y=-delta), 
                         self.current_point.move(x=self.box_width - 4, 
                                                 y=-delta))

