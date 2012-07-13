from taskcardmaker.canvas import Canvas, Point, Image
from taskcardmaker.model import Settings
import taskcardmaker

class QrCodeGenerator (object):
    GOOGLE_CHART_API_URL = "https://chart.googleapis.com/chart?cht=qr&chs=60x60&chl=%s"
    
    def generate_qr_code (self, data):
        url = QrCodeGenerator.GOOGLE_CHART_API_URL % data
        return Image.from_url(url)
    
    @property
    def width (self):
        return 22

    @property
    def height (self):
        return 20


class Renderer (object):
    PAPER_WIDTH = 210
    INITIAL_X = 15
    MAX_LINES_IN_BOX_DESCRIPTION = 5
    
    def __init__ (self, filenameOrFilelikeObject, title=None, author=None):
        self.current_point = Point(Renderer.INITIAL_X, 287)
        self.card_written = False
        self.canvas = Canvas(filenameOrFilelikeObject, title, author)
        self.stories_written = 0
        
        self.settings = Settings()
        self.qr_code_generator = QrCodeGenerator()
        
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
    
            self.render_box((.5, .8, 1))
            self.render_story_box_lines()
            
            self.render_story_identifier(story)
            self.render_story_title(story)
            
            if self.settings.render_qrcode:
                self.canvas.draw_image(self.current_point.move(self.settings.card_width - self.qr_code_generator.width,
                                                               -1 * self.settings.card_width + 1), 
                                       self.qr_code_generator.generate_qr_code(story.identifier))

        for task in story.tasks:
            self.render_task(task)        
        
    def render_task (self, task):
        self.move_to_next_box()

        self.render_box((1, .5, .5) if task.blocker else (1, 1, .5))
        self.render_task_box_lines()
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
        self.canvas.select_font(size=8, family="Helvetica")
        footer = "Made with Taskcardmaker %s - http://taskcardmaker.appspot.com - https://github.com/halimath/taskcardmaker" % taskcardmaker.version
        width = self.canvas.text_width(footer)
        self.canvas.text(Point((Renderer.PAPER_WIDTH - width) / 2, 5), footer) 
            
    def render_story_identifier (self, story):
        self.canvas.fill_color((0, 0, 0))
        self.canvas.select_font(size=self.settings.font_size * 5, family="Helvetica-Bold")
        identifier = self.abbreviate_to_width(story.identifier)
        width = self.canvas.text_width(identifier)
        
        self.canvas.text(self.current_point.move(x=(self.settings.card_width - width) / 2,
                                                 y= -25),
                         identifier)

    def render_story_title (self, story):
        self.canvas.select_font(size=self.settings.font_size * 1.2, family="Helvetica-Bold")
        
        width = self.settings.card_width - 10
        if self.settings.render_qrcode:
            width -= self.qr_code_generator.width
        lines = self.break_into_lines(story.title, width)
        
        i = 0
        for line in lines[0:3]:
            self.canvas.text(self.current_point.move(x=5,
                                                     y= -40 - 6 * i),
                             line)
            i += 1
            
    def render_task_tags (self, task):
        self.canvas.fill_color((0, 0, 0))
        self.canvas.select_font(size=self.settings.font_size * .9, family="Helvetica-Bold")
        tags_string = " | ".join(task.tags)
        width = self.settings.card_width - 4
        if self.settings.render_check_box:
            width -= self.calculate_check_box_width() + 6
        tags_string = self.abbreviate_to_width(tags_string, max_width=width)
        text_width = self.canvas.text_width(tags_string)
        
        self.canvas.text(self.current_point.move(x=(width - text_width) / 2,
                                                 y= -self.settings.card_width + 6),
                         tags_string)
            
    def render_task_title (self, task):
        self.canvas.fill_color((0, 0, 0))
        self.canvas.select_font(size=self.settings.font_size * 1.1, family="Helvetica-Bold")
        title = self.abbreviate_to_width(task.story.identifier,
                                         max_width=self.settings.card_width - 4)
        width = self.canvas.text_width(title)
        
        self.canvas.text(self.current_point.move(x=(self.settings.card_width - width) / 2,
                                                 y= -10), title)
        
    def render_task_description(self, task):
        lines = self.break_into_lines(task.description,
                                      max_width=self.settings.card_width - 10)
        line_number = 1
        if len(lines) > Renderer.MAX_LINES_IN_BOX_DESCRIPTION:
            lines = lines[:Renderer.MAX_LINES_IN_BOX_DESCRIPTION - 1] + ["..."]
        for line in lines:
            self.canvas.text(self.current_point.move(x=5,
                                                     y= -12 - 6 * line_number),
                             line)
            line_number += 1
            
    def abbreviate_to_width (self, text, max_width=None):
        if not max_width:
            max_width = self.settings.card_width
            
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
            
            for word in words:
                if self.canvas.text_width(" ".join(current_line + [word])) > max_width:
                    result.append(" ".join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            
            result.append(" ".join(current_line))
        
        return result            

    def render_box (self, background_color):
        self.canvas.text_color((0, 0, 0))
        self.canvas.fill_color(background_color)
        self.canvas.draw_rect(self.current_point, self.settings.card_width)


    def render_task_box_lines (self):        
        self.canvas.line(self.current_point.move(x=4, y= -12),
                         self.current_point.move(x=self.settings.card_width - 4, y= -12))
        
        self.canvas.fill_color((.4, .4, .4))
        
        
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
        delta = 30
        self.canvas.line(self.current_point.move(x=4, y= -delta),
                         self.current_point.move(x=self.settings.card_width - 4,
                                                 y= -delta))

