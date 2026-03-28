import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

class Task:
    def __init__(self, id, title, description, priority, due_date, completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority  # "High", "Medium", "Low"
        self.due_date = due_date
        self.completed = completed

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return Task(**d)


class TaskManager:
    def __init__(self):
        self.tasks = []
        self._next_id = 1
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            self.tasks = [Task.from_dict(t) for t in data]
            self._next_id = max((t.id for t in self.tasks), default=0) + 1

    def save(self):
        with open(DATA_FILE, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def add(self, title, description, priority, due_date):
        task = Task(self._next_id, title, description, priority, due_date)
        self._next_id += 1
        self.tasks.append(task)
        self.save()
        return task

    def update(self, id, title, description, priority, due_date):
        for t in self.tasks:
            if t.id == id:
                t.title, t.description, t.priority, t.due_date = title, description, priority, due_date
                self.save()
                return

    def delete(self, id):
        self.tasks = [t for t in self.tasks if t.id != id]
        self.save()

    def complete(self, id):
        for t in self.tasks:
            if t.id == id:
                t.completed = True
                self.save()
                return

    def get_filtered(self, view="all", search=""):
        result = self.tasks
        if view == "completed":
            result = [t for t in result if t.completed]
        elif view == "pending":
            result = [t for t in result if not t.completed]
        if search:
            s = search.lower()
            result = [t for t in result if s in t.title.lower() or s in t.description.lower()]
        return result
