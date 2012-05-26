
from taskcardmaker.model import Project, Story, Task

class ParsingError (Exception):
    def __init__ (self, message):
        self.message = message
    
    def __str__ (self):
        return self.message

class TaskCardParser (object):
    def __init__ (self):
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
            identifier, title = line[2:].split("|")
            self.story = Story(identifier.strip(), title.strip())
            self.project.add_story(self.story)
        elif line:
            if not self.story:
                raise ParsingError("No story has been defined")
            
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
