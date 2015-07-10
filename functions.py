from db_init import DBInit
from collection import Collection
from item import Item
import sys
import time
import json
from os.path import isfile, join
from os import listdir, rename, makedirs

class Functions:
    def __init__(self, db, library, stage, verbose):
        self.db = db
        self.library = library
        self.stage = stage
        self.verbose = verbose

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
        process_staging(self)
    
    def printv(self, message):
        if self.verbose:
            print(message)

#Iterate through files and add to collections
def process_staging(functions):
    #Get all files in staging directory
    files = [ f for f in listdir(functions.stage) if isfile(join(functions.stage,f)) ]
    for file in files:
        collection_id = -1
        collection_path = ""
        
        #List collections for user
        functions.list_collections()
        print("N.  New Collection")
        print("File: {}".format(file))
        val = input("Select collection to use (id): ")
        
        #Get or create selected collection
        if val == "N":
            coll = create_collection(functions.library, functions.db)
            collection_id = coll.id 
            collection_path = coll.path
        else:
            coll = Collection.get_by_id(functions.db, int(val))
            collection_id = coll.id 
            collection_path = coll.path
        
        #Assign name and move file
        val = input("Enter a name for {} (if blank filename will be used): ".format(file)) 
        item_name = val
        if item_name == "":
            item_name = file
        item = Item(None, collection_id, item_name, file)
        
        rename(join(functions.stage, file), join(functions.library, collection_path, file))
        
        #Persist
        item.insert(functions.db)

    print("Staging processed!")

#This needs to check for no path collisions.  For now, just make it work
def create_collection(library, db):
    name = ""
    while name == "":
        name = input("Input a name for the collection: ");
    #Figure out how to make a directory here 
    makedirs(join(library,name), exist_ok=True)
    collection = Collection(None, name, name, int(time.time()))
    collection.insert(db)
    return collection
