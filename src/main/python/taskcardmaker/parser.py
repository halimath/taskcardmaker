
from taskcardmaker.model import Project, Story, Task, Settings

class ParsingError (Exception):
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
            self.parse_project_line(line)
        elif line.startswith("S:"):
            self.parse_story_line(line)
        elif line.startswith("#"):
            self.parse_settings_line(line)
        elif line:
            self.parse_task_line(line)
            
    def parse_project_line (self, line):
        self.project = Project(line[2:].strip())
    
    def parse_story_line (self, line):
        if len(line[2:]) == 0:
            raise ParsingError("Missing story identifier")
        try:
            if "|" in line[2:]:
                identifier, title = line[2:].split("|")
                identifier = identifier.strip()
                title = self.split_multiline_artifact(title)
            else:
                identifier = title = line[2:].strip()
            self.story = Story(identifier.strip(), title)
            self.project.add_story(self.story)
        except ValueError:
            raise ParsingError("Syntax error in story line: '%s'" % line)
    
    def parse_task_line (self, line):
        if not self.story:
            raise ParsingError("No story has been defined")
        
        elements = line.split("|")
        
        task = self.split_multiline_artifact(elements[0])
        tags = []
        
        if len(elements) == 2:
            tags = map(lambda x: x.strip(), elements[1].split(','))
            
        blocker = "BLOCKER" in tags
        self.story.add_task(Task(task, tags, blocker))
        
    def parse_settings_line (self, line):
        parts = line[1:].strip().split(' ')
        key = parts[0]
        value = ' '.join(parts[1:])
        if key.lower() == "width":
            try:
                self.settings.card_width = int(value)
            except ValueError:
                raise ParsingError("Invalid card width '%s'" % value)
        elif key.lower() == "font_size":
            try:
                self.settings.font_size = int(value)
            except ValueError:
                raise ParsingError("Invalid font size '%s'" % value)
        elif key.lower() == "checkboxes":
            if value == "yes":
                self.settings.render_check_box = True
            elif value == "no":
                self.settings.render_check_box = False
            else:
                raise ParsingError("Invalid checkboxes value '%s'" % value)
        else:
            raise ParsingError("Unknown setting '%s'" % key)
        
    def split_multiline_artifact (self, artifact):
        return [line.strip() for line in artifact.split("\\")]
