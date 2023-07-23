from decouple import config
from pymongo import MongoClient
from models.projects import Project

class Database:
    def __init__(self):
        self.client = MongoClient(config("MONGO_URI"))
        self.db = self.client.get_database("whoisdg")
        self.project_collection = self.db.get_collection("project")

    def get_projects(self):
        return list(self.project_collection.find({'include': True}))
