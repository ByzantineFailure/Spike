import sqlite3

class DBInit:
    def init_db(library):
        conn = sqlite3.connect(library, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute('''PRAGMA foreign_keys = ON;''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS collections (
                id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                last_modified DATETIME NOT NULL
            );''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                collection_id INTEGER,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                FOREIGN KEY (collection_id) references collections(id) ON DELETE CASCADE
            );''')
        conn.commit()
        conn.close()
