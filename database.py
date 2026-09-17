import sqlite3

class Database():
    def __init__(self):
        self.create_table()
        
    def create_table(self):
        with sqlite3.connect("database.db") as connection:
            cursor=connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users 
            (user_names TEXT UNIQUE NOT NULL,password_users TEXT NOT NULL ,user_number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL  )''')
         
            cursor.execute('''CREATE TABLE IF NOT EXISTS note
            (note_number INTEGER PRIMARY KEY AUTOINCREMENT,notes TEXT NOT NULL ,title_note TEXT NOT NULL ,create_at NOT NULL ,user_number INTEGER ,FOREIGN KEY(user_number)  REFERENCES users(user_number))''')

    def register(self,user_names,password_users):
        with sqlite3.connect("database.db") as connection:
            cursor =connection.cursor()
            cursor.execute('''INSERT INTO users (user_names,password_users) VALUES(?,?)''',(user_names,password_users))
            return True

    def check_username (self,user_names):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT user_names FROM users WHERE user_names=?''',(user_names,))
            return cursor.fetchall()

    
    def insert_note(self,notes,title_note):
        with sqlite3.connect("database.db") as connection:
            cursor=connection.cursor()
            cursor.execute('''INSERT INTO note (notes,title_note,create_at)  VALUES(?,?,0)''',(notes,title_note))
            return cursor.lastrowid

    def delete_note(self,note_number):
        with sqlite3.connect("database.db") as connection:
            cursor =connection.cursor()
            cursor.execute('''DELETE FROM note WHERE note_number=?''',(note_number,))
            return True

    def get_notes(self):
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT title_note FROM note ''')
            return cursor.fetchall()

    def change_note(self,title_note,note_number):
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE note SET title_note=? WHERE note_number=?''',(title_note,note_number))
    

    def get_note(self,note_number):
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT  title_note FROM note WHERE note_number=?''',(note_number,))
            return cursor.fetchone()