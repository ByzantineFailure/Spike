from db_init import DBInit
from collection import Collection
from item import Item
import sys
import time
import json
from os.path import isfile, join
from os import listdir, rename, makedirs

class Functions:
    def __init__(self, db, library, stage):
        self.db = db
        self.library = library
        self.stage = stage

    def init_db(self):
        DBInit.init_db(self.db)

    def list_collections(self):
        collections = Collection.get_all(self.db)
        print("COLLECTIONS")
        Collection.print_table_header()
        for collection in collections:
            collection.print_for_table()
    
    def display_collection(self, id):
        collection = Collection.get_by_id(self.db, id);
        if collection == None:
            raise Exception("No collection with id {}!".format(id))
        Collection.print_table_header()
        collection.print_for_table()
        items = Item.get_by_collection(self.db, collection.id)
        print("ITEMS")
        Item.print_table_header()
        for item in items:
            item.print_for_table()
        
    def display_item(self, id):
        item = Item.get_by_id(self.db, id);
        if item == None:
            raise Exception("No item with id {}!".format(id))
        Item.print_table_header()
        item.print_for_table()
    
    def delete_collection(self, id):
        collection = Collection.get_by_id(self.db, id);
        collection.delete();

    def delete_item(self, id):
        item = Item.get_by_id(self.db, id);
        item.delete();
    
    def process_staging(self):
        process_staging(self.stage, self.library, self)

#Iterate through files and add to collections
def process_staging(stage, library, functions):
    #Get all files in staging directory
    files = [ f for f in listdir(stage) if isfile(join(stage,f)) ]
    for file in files:
        collection_id = -1
        collection_path = ""
        
        #List collections for user
        print_collections()
        print("N.  New Collection")
        print("File: {}".format(file))
        val = input("Select collection to use: ")
        
        #Get or create selected collection
        if val == "N":
            coll = create_collection(library)
            collection_id = coll.id 
            collection_path = coll.path
        else:
            usable_cols = [ c for c in collections if c.id == int(val) ]
            if len(usable_cols) == 0:
                print("Could not find collection with id {}!  Skipping file...".format(val))
                continue
            else:
                collection_id = usable_cols[0].id 
                collection_path = usable_cols[0].path
        
        #Assign name and move file
        val = input("Enter a name for the item (if blank filename will be used): ") 
        item_name = val
        if item_name == "":
            item_name = file
        item = Item(None, collection_id, item_name, file)
        
        rename(join(stage, file), join(library, collection_path, file))
        
        #Persist
        item.insert()

    print("Staging processed!")

#This needs to check for no path collisions.  For now, just make it work
def create_collection(library):
    name = ""
    while name == "":
        name = input("Input a name for the collection: ");
    #Figure out how to make a directory here 
    makedirs(join(library,name), exist_ok=True)
    collection = Collection(None, name, name, int(time.time()))
    collection.insert()
    return collection
