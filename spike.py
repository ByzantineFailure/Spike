#!/usr/local/bin/python3
import argparse
from functions import Functions
from scan_existing import DirectoryInit
from os.path import join
from os import makedirs

parser = argparse.ArgumentParser(description="An assistant for your library (of files)")
parser.add_argument("--lib_db", type=str, help="Specify library.db's location", default=join('library', 'library.db'))
parser.add_argument("--lib_dir", type=str, help="Specify the library directory", default="library")
parser.add_argument("--stage_dir", type=str, help="Specify the staging directory", default="stage")
parser.add_argument("--verbose", help="Set to verbose mode", action="store_true")

group = parser.add_mutually_exclusive_group()
group.add_argument("--init", action="store_true", help="Init and store a library")
group.add_argument("-l", "--list_collections", action="store_true", help="List all collections")
group.add_argument("-c", "--display_collection", type=int, default=-1, help="Display the collection with the specified id")
group.add_argument("-i", "--display_item", type=int, default=-1, help="Delete the item with the specified id")
group.add_argument("--del_coll", type=int, default=-1, help="Delete the collection with the specified id")
group.add_argument("--del_item", type=int, default=-1, help="Delete the item with the specified id")
group.add_argument("-p", "--process", action="store_true", help="Process the staging directory")

args = parser.parse_args()

functions = Functions(args.lib_db, args.lib_dir, args.stage_dir, args.verbose)

#todo: Check existence of stage, library, and db
makedirs(args.lib_dir, exist_ok=True)
makedirs(args.stage_dir, exist_ok=True)

functions.init_db()

if args.init:
    print("Init with the following settings (Structure of 'library' will be inited as collection)?")
    print("Database location: " + args.lib_db)
    print("Library location: " + args.lib_dir)
    print("WARNING:  THIS WILL MOVE ALL FILES IN 2ND LEVEL DIRECTORIES AND LOWER")
    print("          INTO THE FIRST-LEVEL DIRECTORY.")
    choice = input("Y/N : ")
    if choice == "Y" or choice == "y":
        scanner = DirectoryInit(args.lib_db, args.lib_dir, args.verbose)
        scanner.init_library(); 
    else:
        print("Init cancelled.")

elif args.list_collections:
    functions.list_collections()
elif args.display_collection >= 0:
    functions.display_collection(args.display_collection)
elif args.display_item >= 0:
    functions.display_item(args.display_item)
elif args.del_coll >= 0:
    functions.display_collection(args.del_coll);
    selection = input("Are you sure you want to delete this collection (Y/N)? ")
    if selection == "Y":
        functions.delete_collection(args.del_coll)
    else:
        print("Did not delete collection")
elif args.del_item >= 0:
    functions.display_item(args.del_item);
    selection = input("Are you sure you want to delete this item (Y/N)? ")
    if selection == "Y":
        functions.delete_item(args.del_item)
    else:
        print("Did not delete item")
elif args.process:
    functions.process_staging()
else:
    print("No operation specified (-h for help)")
