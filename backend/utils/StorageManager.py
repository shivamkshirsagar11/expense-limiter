from dataclasses import dataclass
from core.config import settings
import json
import os
from utils.logger import create_logger, log_debug_and_info

LOGGER = create_logger(os.path.basename(__file__))

MANAGER = None

@dataclass
class JsonManager:
    db: dict

    def __getitem__(self, key):
        LOGGER.debug("Getting key %s", key)
        searchSpace = self.db
        keys = key.split(".")
        
        for k in keys:
            if k not in searchSpace:
                searchSpace = {}
            else:
                searchSpace = searchSpace[k]
        LOGGER.debug("Returning key=value %s=%s", key, searchSpace)
        return searchSpace
    
    def __setitem__(self, key, value):
        LOGGER.debug("Setting key=value %s=%s", key, searchSpace)
        searchSpace = self.db
        *keys, lastKey = [*key.split(".")]
        
        for k in keys:
            if k not in searchSpace:
                searchSpace = {}
            else:
                searchSpace = searchSpace[k]
        
        searchSpace[lastKey] = value
    
    def __delitem__(self, key):
        LOGGER.debug("Deleting key %s", key)
        searchSpace = self.db
        *keys, lastKey = [*key.split(".")]
        
        for k in keys:
            if k not in searchSpace:
                searchSpace = {}
            else:
                searchSpace = searchSpace[k]
        
        del searchSpace[lastKey]
    
    def __contains__(self, key):
        LOGGER.debug("Checking if key %s is in database", key)
        searchSpace = self.db
        *keys, lastKey = [*key.split(".")]
        
        for k in keys:
            if k not in searchSpace:
                searchSpace = {}
            else:
                searchSpace = searchSpace[k]
        LOGGER.debug("Key %s is %s the database", key, ("in" if lastKey in searchSpace else "not in"))
        return lastKey in searchSpace

    def get_immidiate_parent_limit(self, key):
        log_debug_and_info(LOGGER, f"Getting immidiate limit of {key}")
        if not key:
            Err = "Section name must be specified"
            LOGGER.error(Err)
            raise RuntimeError(Err)

        parent_chain = key.split(".")
        if len(parent_chain) == 1:
            LOGGER.debug("Limit of %s is %s which is immidiate parent of %s", parent_chain, settings.LITERAL.INF, parent_chain)
            return settings.LITERAL.INF
        else:
            parent = '.'.join(parent_chain[:-1])
            LOGGER.debug("Limit of %s is %s which is immidiate parent of %s", parent, self[parent]['limit'], parent_chain[1])
            return self[parent]['limit']
    
    def get_propagated_limit_for_child(self, key):
        log_debug_and_info(LOGGER, f"Getting the remaining limit for new section to be added {key}")
        if not key:
            Err = "Section name must be specified"
            LOGGER.error(Err)
            raise RuntimeError(Err)

        parent_chain = key.split(".")
        if len(parent_chain) == 1:
            LOGGER.debug("%s is root, so just returning it's limit", key)
            return self[parent_chain[0]]['limit']
        else:
            LOGGER.debug("%s is not root, we will need to calculate ramining amount that can be limit for new section", key)
            parent = '.'.join(parent_chain[:-1])
            remaining_limit = self[parent]['limit']
            
            for section, value in self[parent].items():
                if section not in settings.LITERAL.SECTION_CONSTANT_TUPLE:
                    remaining_limit -= value['limit']
            
            return remaining_limit
            


class StorageManager(JsonManager):
    def __init__(self, path: str):
        log_debug_and_info(LOGGER, f"Creating storage manager for path:{path}")
        self.path = path
        
        # Ensure directory exists
        log_debug_and_info(LOGGER, "Creating directory if does not exists")
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Create file if it doesn't exist
        if not os.path.exists(path):
            log_debug_and_info(LOGGER, "Creating file, it does not exists")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({}, f)

        # Check if file is empty
        if os.path.getsize(path) == 0:
            log_debug_and_info(LOGGER, "File is empty, so initialising data")
            data = {}
        else:
            log_debug_and_info(LOGGER, "Reading database file")
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

        super().__init__(data)
    
    def save(self):
        LOGGER.debug("Saving cumulative content in the database")
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=4)
        LOGGER.debug("Cumulative content saved")
    

def get_storage_manager():
    global MANAGER
    if MANAGER:
        return MANAGER
    else:
        MANAGER = StorageManager(settings.STORAGE.PATH)
        return MANAGER
