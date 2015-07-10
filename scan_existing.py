import os
import time
import json
from os import rename
from os.path import join, isfile, islink
from item import Item
from collection import Collection
from db_init import DBInit

class DirectoryInit:
    def __init__(self, db, library, verbose):
        self.db = db
        self.library = library
        self.verbose = verbose

    def init_library(self):
        self.print("DB initting...")
        DBInit.init_db(self.db)
        self.print("DB init'd successfully")
        self.print("Scanning {}...".format(self.library))
        for file in os.listdir(self.library):
            if isfile(file) or islink(file):
                self.print("{} is file or symlink, skipping...".format(file))
                continue
            else:
                self.print("{} is top-level directory.  Initting collection...".format(file))
                self.__init_directory(file, join(self.library, file), file)
             
    def __init_directory(self, collection_name, directory_path, dest_dir):
        collection = Collection(None, collection_name, collection_name, int(time.time()))
        self.print("Collection init'd as {}".format(json.dumps(collection.__dict__)))
        collection.insert(self.db)
        
        self.__init_subdir(directory_path, collection.id, directory_path)
    
    def __init_subdir(self, collection_path, collection_id, current_path):
        is_root = collection_path == current_path
        self.print("Processing directory: {}".format(current_path))

        for file in os.listdir(current_path):
            item_name = file
            new_name = join(collection_path, item_name)
            current_file = join(current_path, item_name)

            if isfile(current_file) and not islink(current_file):
                self.print("Found file {}".format(current_file))
                if not is_root and isfile(new_name):
                    self.print("{} has duplicate. Prepending timestamp.".format(current_file))
                    item_name = "{} - {}".format(int(time.time()), file)
                    new_name = join(collection_path, item_name) 
                
                rename(current_file, new_name)
                item = Item(None, collection_id, item_name, item_name)
                item.insert(self.db)
                print("Item created: {}".format(json.dumps(item.__dict__)))
            else:
                self.print("Found subdirectory: {}".format(current_file))
                self.__init_subdir(collection_path, collection_id, join(current_path, file))
                
    def print(self, message):
        if self.verbose:
            print(message)
