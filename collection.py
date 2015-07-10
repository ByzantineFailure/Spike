import sqlite3

def get_connection(library):
    return sqlite3.connect(library, detect_types=sqlite3.PARSE_DECLTYPES)

select_all = '''SELECT id, name, path, last_modified FROM collections;'''
select_by_id = '''SELECT id, name, path, last_modified FROM collections WHERE id = ?;'''
select_by_name = '''SELECT id, name, path, last_modified FROM collections WHERE name = ?;'''
delete_by_id = '''DELETE FROM collections WHERE id = ?;'''
insert_collection = '''INSERT INTO collections (name, path, last_modified) VALUES (?, ?, ?);'''
update_collection = '''UPDATE collections SET name = ?, path = ?, last_modified = ? WHERE id = ?;'''

name_width = 34
path_width = 33
id_width = 9

def pad_to_width(original, width):
    if len(original) >= width:
        return original        
    return original + space_str[0:width - len(original)]

space_str = "                                              "

class Collection:
    def __init__(self, id, name, path, last_modified):
        self.id = id
        self.name = name
        self.path = path
        self.last_modified = last_modified
    
    #TODO:  Format timestamp to readable date
    def print_for_table(self):
        print("{}|{}|{}|{}".format(pad_to_width(str(self.id), id_width), 
            pad_to_width(self.name, name_width), pad_to_width(self.path, path_width),
            str(self.last_modified)))
    
    def print_table_header():
        print("id       | Name                             | path                            | modified ")
        print("===========================================================================================")

    def get_all(library):
        conn = get_connection(library) 
        cursor = conn.cursor();
        collections = []
       
        for row in cursor.execute(select_all):
            collections.append(Collection(row[0], row[1], row[2], row[3]))    
        
        conn.close()
        return collections
    
    def get_by_id(library, id):
        conn = get_connection(library)
        cursor = conn.cursor()
        cursor.execute(select_by_id, (id,))

        result = cursor.fetchall()
        
        if len(result) == 0:
            return None
        else:
            row = result[0]
            return Collection(row[0], row[1], row[2], row[3])
        
        conn.close()
    
    def get_by_name(library, name):
        conn = get_connection(library)
        cursor = conn.cursor()
        cursor.execute(select_by_name, (name,))

        result = cursor.fetchall()
        
        if len(result) == 0:
            return None
        else:
            row = result[0]
            return Collection(row[0], row[1], row[2], row[3])
        
        conn.close()
        

    def insert(self, library):
        if not self.id == None:
            raise Exception('Cannot insert collection with an id')

        conn = get_connection(library);
        cursor = conn.cursor();
        cursor.execute(insert_collection, (self.name, self.path, self.last_modified))
        self.id = cursor.lastrowid
        
        conn.commit()
        conn.close()
    
    def update(self, library):
        if self.id == None:
            raise Exception('Cannot update a collection without an id')
        
        conn = get_connection(library);
        cursor = conn.cursor();
        cursor.execute(update_collection, (self.name, self.path, self.last_modified, self.id))

        conn.commit()
        conn.close()

    def delete(self, library):
        conn = get_connection(library) 
        cursor = conn.cursor();
        
        cursor.execute(delete_by_id, (self.id,))
        conn.commit()
        conn.close()
        self.id = None
