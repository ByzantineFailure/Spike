# Spike
An assistant for your library (of files)

usage: spike [-h] [--lib_db LIB_DB] [--lib_dir LIB_DIR]

             [--stage_dir STAGE_DIR] [--verbose]
             
             [--init | -l | -c DISPLAY_COLLECTION | -i DISPLAY_ITEM | --del_coll DEL_COLL | --del_item DEL_ITEM | -p]


An assistant for your library (of files)


optional arguments:

  -h, --help            show this help message and exit
  
  --lib_db LIB_DB       Specify library.db's location
  
  --lib_dir LIB_DIR     Specify the library directory
  
  --stage_dir STAGE_DIR
  
                        Specify the staging directory
                        
  --verbose             Set to verbose mode
  
  --init                Init and store a library
  
  -l, --list_collections
  
                        List all collections
                        
  -c DISPLAY_COLLECTION, --display_collection DISPLAY_COLLECTION
  
                        Display the collection with the specified id
                        
  -i DISPLAY_ITEM, --display_item DISPLAY_ITEM
  
                        Delete the item with the specified id
                        
  --del_coll DEL_COLL   Delete the collection with the specified id
  
  --del_item DEL_ITEM   Delete the item with the specified id
  
  -p, --process         Process the staging directory
