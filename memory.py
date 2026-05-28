import json
import os

MEMORY_FILE = 'memory.json'

class Memory:
    def __init__(self, filepath=MEMORY_FILE):
        self.filepath = filepath
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = []
        else:
            self.data = []

    def _save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_record(self, record):
        self.data.append(record)
        self._save()

    def get_all(self):
        return self.data
