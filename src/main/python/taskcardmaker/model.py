
def string_or_list_as_list (string_or_list):
    if isinstance(string_or_list, list):
        return string_or_list
    else:
        return [str(string_or_list)]


class Settings (object):
    COLORS_FOREGROUND = "foreground"
    COLORS_BACKGROUND = "background"

    def __init__ (self):
        self.card_width = 80
        self.font_size = 14
        self.render_check_box = False
        self.render_storycards = True
        self.colors = Settings.COLORS_BACKGROUND

    def as_map (self):
        return {
            'cardWidth': self.card_width,
            'fontSize': self.font_size,
            'renderCheckBox': self.render_check_box,
            'renderStorycards': self.render_storycards,
            'colors': self.colors
        }

class Project (object):
    def __init__ (self, name=None):
        self.name = name or ""
        self.stories = []
        
    def add_story (self, story):
        self.stories.append(story)
        story.project = self
        
    def as_map (self):
        return { 
                "name": self.name,
                "stories": map(lambda x: x.as_map(), self.stories)
                }

class Story (object):
    def __init__ (self, identifier, title=None):
        self.project = None
        self.identifier = identifier
        
        self.title = string_or_list_as_list(title if title else identifier)
        self.tasks = []
        
    @property
    def name (self):
        return "%s [%s]" % (self.title, self.identifier)
        
    def add_task (self, task):
        self.tasks.append(task)
        task.story = self
        
    def as_map (self):
        return { 
                "identifier": self.identifier,
                "title": self.title,
                "tasks": map(lambda x: x.as_map(), self.tasks)
                }


class Task (object):
    def __init__ (self, description, tags=None, blocker=False):
        self.story = None
        self.description = []
        
        self.description = string_or_list_as_list(description)
        
        self.tags = []
        if tags:
            for tag in tags:
                self.tags.append(tag)
        self.blocker = blocker

    def as_map (self):
        return { 
                "description": self.description,
                "tags": self.tags,
                "blocker": self.blocker
                }
