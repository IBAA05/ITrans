import sqlite3


class Dao:
    DATABASE_PATH = __file__ + "./../" + "database.db"
    
    def __init__ (self) :
        
        try:
            self.conn = sqlite3.connect(self.DATABASE_PATH)  
            self.cursor = self.conn.cursor ()
        except sqlite3.Error as e:
            self.close()

    def  createSchema(self)  : 
        sql_statements  = [    
               """DROP TABLE IF EXISTS station_going ;
               """, 
               """ CREATE TABLE station_going(
                    id INTEGER PRIMARY KEY ,
                        name_ar TEXT NOT NULL,
                        name_en TEXT NOT NULL,
                         name_fr TEXT NOT NULL,
                        lat DECIMAL NOT NULL,
                        lng DECIMAL NOT NULL,
                        ord INT NOT NULL);
               """  , 
               """DROP TABLE IF EXISTS station_returning
               """,
               """CREATE TABLE station_returning (
                    id INTEGER PRIMARY KEY  ,
                    name_ar TEXT NOT NULL,
                    name_en TEXT NOT NULL,
                    name_fr TEXT NOT NULL,
                    lat DECIMAL NOT NULL,
                    lng DECIMAL NOT NULL ,
                    ord INT NOT NULL
                 ) ;
               """, 
               """Drop TABLE IF EXISTS interstation_going;
               """ , 
               """CREATE TABLE interstation_going(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lat DECIMAL NOT NULL ,
                        lng DECIMAL NOT NULL ,
                        from_station INT NOT NULL ,
                        to_station INT NOT NULL 
                 );
               """,  
                """Drop TABLE IF EXISTS interstation_returning;
               """ , 
               """CREATE TABLE interstation_returning(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lat DECIMAL NOT NULL ,
                        lng DECIMAL NOT NULL ,
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
                       value TEXT NOT NULL
                       );
               """,
                """Drop TABLE IF EXISTS log
               """, 
               """  CREATE TABLE log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        message TEXT NOT NULL,
                        sender TEXT NOT NULL,
                        receiver TEXT NOT NULL,
                        received_at INTEGER NOT NULL      
                   );
               """, 
               """Drop TABLE IF EXISTS ride
               """, 
               """   CREATE TABLE ride (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        line INTEGER NOT NULL,
                        direction TEXT NOT NULL,
                        started_at INTEGER NOT NULL,
                        finished_at INTEGER     
                   );
               """,
               """Drop TABLE IF EXISTS calibrate
               """,
                """   CREATE TABLE calibrate (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        location TEXT NOT NULL , 
                        position TEXT NOT NULL  
                   );
               """   
               ]
      
        for statement in sql_statements:
            self.cursor.execute(statement)
            
    def close (self) : 
        self.conn.close()


