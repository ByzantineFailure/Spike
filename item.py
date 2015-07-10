import sqlite3

def get_connection(library):
    return sqlite3.connect(library, detect_types=sqlite3.PARSE_DECLTYPES)

select_all = '''SELECT id, collection_id, name, path FROM items;'''
select_by_id = '''SELECT id, collection_id, name, path FROM items WHERE id = ?;'''
select_by_collection = '''SELECT id, collection_id, name, path FROM items WHERE collection_id = ?;'''
delete_by_id = '''DELETE FROM items WHERE id = ?;'''
insert_item = '''INSERT INTO items (collection_id, name, path) VALUES (?, ?, ?);'''
update_item = '''UPDATE items SET collection_id = ?, name = ?, path = ? WHERE id = ?;'''

name_width = 34
path_width = 33
id_width = 9
coll_id_width = 10

def pad_to_width(original, width):
    if len(original) >= width:
        return original        
    return original + space_str[0:width - len(original)]

space_str = "                                              "

class Item:
    def __init__(self, id, collection_id, name, path):
        self.id = id
        self.collection_id = collection_id
        self.name = name
        self.path = path
    
    #TODO:  Format timestamp to readable date
    def print_for_table(self):
        print("{}|{}|{}|{}".format(pad_to_width(str(self.id), id_width), 
            pad_to_width(str(self.collection_id), coll_id_width), pad_to_width(self.name, name_width),
            pad_to_width(self.path, path_width)))
    
    def print_table_header():
        print("id       | coll_id  | Name                             | path                            ")
        print("===========================================================================================")

    def get_all(library):
        conn = get_connection(library) 
        cursor = conn.cursor();
        items = []
       
        for row in cursor.execute(select_all):
            items.append(Item(row[0], row[1], row[2], row[3]))    
        
        conn.close()
        return items
        
    def get_by_id(library, id):
        conn = get_connection(library)
        cursor = conn.cursor()
        cursor.execute(select_by_id, (id,))

        result = cursor.fetchall()
        
        if len(result) == 0:
            return None
        else:
            row = result[0]
            return Item(row[0], row[1], row[2], row[3])
        
        conn.close()

    def get_by_collection(library, collection_id):
        conn = get_connection(library) 
        cursor = conn.cursor();
        items = []
       
        for row in cursor.execute(select_by_collection, (collection_id,)):
            items.append(Item(row[0], row[1], row[2], row[3]))    
        
        conn.close()
        return items

    def insert(self, library):
        if not self.id == None:
            raise Exception('Cannot insert item with an id')

        conn = get_connection(library);
        cursor = conn.cursor();
        cursor.execute(insert_item, (self.collection_id, self.name, self.path))
        self.id = cursor.lastrowid
        
        conn.commit()
        conn.close()
    
    def update(self, library):
        if self.id == None:
            raise Exception('Cannot update an item without an id')
        
        conn = get_connection(library);
        cursor = conn.cursor();
        cursor.execute(update_item, (self.collection_id, self.name, self.path, self.id))

        conn.commit()
        conn.close()
    
    def delete(self, library):
        conn = get_connection(library) 
        cursor = conn.cursor();
        
        cursor.execute(delete_by_id, (self.id,))
        conn.commit()
        conn.close()
        self.id = None
    
