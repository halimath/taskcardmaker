import getpass
import reportlab.pdfgen.canvas
import reportlab.lib.pagesizes
import reportlab.lib.units


class Point (object):
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        
    def __add__ (self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return Point(self.x + other, self.y + other)
    
    def move (self, x=0, y=0):
        return Point(self.x + x, self.y + y)
    
class Canvas (object):
    def __init__ (self, filenameOrFilelikeObject, title=None, author=None):
        self.canvas = reportlab.pdfgen.canvas.Canvas(filenameOrFilelikeObject,
                                                     pagesize=reportlab.lib.pagesizes.A4)
        if title:
            self.canvas.setTitle(title)
        if not author:
            author = getpass.getuser()
        self.canvas.setAuthor(author)
        self.scaling = reportlab.lib.units.mm
        
    def close (self):
        self.canvas.showPage()
        self.canvas.save()
        
    def fill_color (self, rgb, alpha=1):
        self.canvas.setFillColorRGB(rgb[0], rgb[1], rgb[2], alpha)
        
    def text_color (self, rgb, alpha=1):
        self.canvas.setStrokeColorRGB(rgb[0], rgb[1], rgb[2], alpha)

    def select_font (self, family=None, size=None):
        if family:
            self.canvas.setFont(family, size)
        if size:        
            self.canvas.setFontSize(size)
    
    def text_width (self, text):
        return self.canvas.stringWidth(text) / self.scaling
            
    def text (self, position, text):
        self.canvas.drawString(position.x * self.scaling, 
                               position.y * self.scaling, 
                               text)
        return self
    
    def fill_rect (self, upper_left, width, height=None):
        if not height:
            height = width
        self.canvas.rect(upper_left.x * self.scaling, 
                         (upper_left.y - height) * self.scaling, 
                         width * self.scaling, 
                         height * self.scaling, 
                         fill=1)
    
    def line (self, start_point, end_point):
        self.canvas.line(start_point.x * self.scaling, 
                         start_point.y * self.scaling, 
                         end_point.x * self.scaling, 
                         end_point.y * self.scaling)
        return self
    
    def next_page (self):
        self.canvas.showPage()