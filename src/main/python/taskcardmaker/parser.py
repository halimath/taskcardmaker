
from taskcardmaker.model import Project, Story, Task, Settings

class SyntaxError (Exception):
    def __init__ (self, message):
        self.message = message
    
    def __str__ (self):
        return self.message

class TaskCardParser (object):
    def __init__ (self):
        self.settings = Settings()
        self.project = Project()
        self.story = None
        
    def parse (self, *lines):
        for line in lines:
            self.parse_line(line)
    
    def parse_line (self, line):
        line = line.strip()
        
        if line.startswith("P:"):
            self.project = Project(line[2:].strip())
        elif line.startswith("S:"):
            if len(line[2:]) == 0:
                raise SyntaxError("Missing story identifier")
            try:
                if "|" in line[2:]:
                    identifier, title = line[2:].split("|")
                else:
                    identifier = title = line[2:]
                self.story = Story(identifier.strip(), title.strip())
                self.project.add_story(self.story)
            except ValueError:
                raise SyntaxError("Syntax error in story line: '%s'" % line)
        elif line.startswith("#"):
            self.parse_settings_line(line)
        elif line:
            if not self.story:
                raise SyntaxError("No story has been defined")
            
            blocker = False
            if line.startswith("B:"):
                blocker = True
                line = line[2:]
            
            elements = line.split("|")
            
            task = elements[0]
            tags = None
            
            if len(elements) == 2:
                tags = map(lambda x: x.strip(), elements[1].split(','))
                
            self.story.add_task(Task(task.strip(), tags, blocker))
    
    def parse_settings_line (self, line):
        parts = line[1:].strip().split(' ')
        key = parts[0]
        value = ' '.join(parts[1:])
        if key.lower() == "width":
            try:
                self.settings.card_width = int(value)
            except ValueError:
                raise SyntaxError("Invalid card width '%s'" % value)
        elif key.lower() == "font_size":
            try:
                self.settings.font_size = int(value)
            except ValueError:
                raise SyntaxError("Invalid font size '%s'" % value)
        else:
            raise SyntaxError("Unknown setting '%s'" % key)
