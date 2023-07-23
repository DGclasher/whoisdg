
class Project:
    def __init__(self, name, description, github_link=None, web_link=None, include=True):
        self.name = name
        self.description = description
        self.github_link = github_link
        self.web_link = web_link
        self.include = include

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "github_link": self.github_link,
            "web_link": self.web_link,
            "include": self.include
        }
