from dataclasses import dataclass
from core.config import settings
import json
import os

MANAGER = None

@dataclass
class JsonManager:
    db: dict

    def __getitem__(self, key):
        searchSpace = self.db
        keys = key.split(".")
        
        for k in keys:
            if k not in searchSpace:
                searchSpace = {}
            else:
                searchSpace = searchSpace[k]
        
        return searchSpace
    
    def __setitem__(self, key, value):
        searchSpace = self.db
        *keys, lastKey = [*key.split(".")]
        
        for k in keys:
            if k not in searchSpace:
                searchSpace = {}
            else:
                searchSpace = searchSpace[k]
        
        searchSpace[lastKey] = value
    
    def __delitem__(self, key):
        searchSpace = self.db
        *keys, lastKey = [*key.split(".")]
        
        for k in keys:
            if k not in searchSpace:
                searchSpace = {}
            else:
                searchSpace = searchSpace[k]
        
        del searchSpace[lastKey]
    
    def __contains__(self, key):
        searchSpace = self.db
        *keys, lastKey = [*key.split(".")]
        
        for k in keys:
            if k not in searchSpace:
                searchSpace = {}
            else:
                searchSpace = searchSpace[k]
        
        return lastKey in searchSpace


class StorageManager(JsonManager):
    def __init__(self, path: str):
        
        self.path = path
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Create file if it doesn't exist
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({}, f)

        # Check if file is empty
        if os.path.getsize(path) == 0:
            data = {}
        else:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

        super().__init__(data)
    
    def save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=4)
    

def get_storage_manager():
    global MANAGER
    if MANAGER:
        return MANAGER
    else:
        MANAGER = StorageManager(settings.STORAGE.PATH)
        return MANAGER
