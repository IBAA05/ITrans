import sqlite3 



class Dao  : 
    
    DATABASE_PATH  = "database.db" 
    
    def __init__ (self) :
        
        try:
            self.conn = sqlite3.connect(self.DATABASE_PATH)  
            self.cursor = self.conn.cursor ()
        except sqlite3.Error as e:
            self.close()

    def  createSchema(self)  : 
        sql_statements  = [ 
               """DROP TABLE IF EXISTS going .
               """, 
               """ CREATE TABLE going(
                    id INTEGER PRIMARY KEY ,
                        name_ar TEXT NOT NULL,
                        name_en TEXT NOT NULL,
                         name_fr TEXT NOT NULL,
                        lat DECIMAL NOT NULL,
                        long DECIMAL NOT NULL,
                        ord INT NOT NULL);
               """  , 
               """"DROP TABLE IF EXISTS returning
               """,
               """CREATE TABLE returning (
                    id INTEGER PRIMARY KEY  ,
                    name_ar TEXT NOT NULL,
                    name_en TEXT NOT NULL,
                    name_fr TEXT NOT NULL,
                    lat DECIMAL NOT NULL,
                    long DECIMAL NOT NULL ,
                    ord INT NOT NULL
                 ) ;
               """, 
               """Drop TABLE IF EXISTS interstation_going
               """ , 
               """CREATE TABLE interstation_going(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lat DECIMAL NOT NULL ,
                        long DECIMAL NOT NULL ,
                        from_station INT NOT NULL ,
                        to_station INT NOT NULL 
                 );
               """,  
                """Drop TABLE IF EXISTS interstation_returning
               """ , 
               """CREATE TABLE interstation_returning(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lat DECIMAL NOT NULL ,
                        long DECIMAL NOT NULL ,
                        from_station INT NOT NULL ,
                        to_station INT NOT NULL 
                 );
               """,
               """Drop TABLE IF EXISTS config
               """, 
               """
                  CREATE TABLE config (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       key TEXT  NOT NULL ,
                       value TEXT NOT NUL
               """      
               ]
      
        for statement in sql_statements:
            self.cursor.execute(statement)
            
    def close (self) : 
        self.conn.close()

    