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
        self.title = title if title else identifier
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
        self.description = description
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
