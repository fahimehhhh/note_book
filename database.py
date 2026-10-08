import sqlite3
import os
class Database():
    def __init__(self):
        self.create_table()
        
    def create_table(self):
        with sqlite3.connect("database.db") as connection:
            cursor=connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users 
            (user_names TEXT UNIQUE NOT NULL,password_hash TEXT NOT NULL ,user_number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, token_users TEXT UNIQUE )''')
         
            cursor.execute('''CREATE TABLE IF NOT EXISTS note
            (note_number INTEGER PRIMARY KEY AUTOINCREMENT,notes TEXT NOT NULL ,title_note TEXT NOT NULL ,create_at INTEGER NOT NULL ,user_number INTEGER ,priority TEXT NOT NULL DEFAULT 'low',FOREIGN KEY(user_number)  REFERENCES users(user_number) )''')
    
    def get_user_number(self,token_user):
        with sqlite3.connect('database.db') as connection:
            cursor=connection.cursor()
            cursor.execute('''SELECT user_number FROM users WHERE token_users=?''',(token_user,))
            return cursor.fetchone()
   
    def register(self,user_names,password_hash):
        with sqlite3.connect("database.db") as connection:
            cursor =connection.cursor()
            cursor.execute('''INSERT INTO users (user_names,password_hash) VALUES(?,?)''',(user_names,password_hash))
            return 

    def login(self,token_user ,user_names):
        with sqlite3.connect("database.db") as connection:
            cursor =connection.cursor()
            cursor.execute('''UPDATE  users SET token_users=?  WHERE user_names=?''',(token_user,user_names))
            cursor.execute('''SELECT token_users FROM users WHERE user_names=?''',(user_names,))
            return cursor.fetchone()

    def check_username(self,user_name):
        with sqlite3.connect("database.db") as connection:
            cursor=connection.cursor()
            cursor.execute('''SELECT user_names FROM users WHERE user_names=?''',(user_name,))
            return cursor.fetchone()

    def check_password(self,user_name):
        with sqlite3.connect('database.db') as connection:
            cursor=connection.cursor()
            cursor.execute('''SELECT password_hash FROM users WHERE user_names=?''',(user_name,))
            return cursor.fetchone()


    def insert_note(self,notes,title_note,priority,user_number):
        with sqlite3.connect("database.db") as connection:
            cursor=connection.cursor()
            cursor.execute('''INSERT INTO note (notes,title_note,priority,user_number,create_at)  VALUES(?,?,?,?,0)''',(notes,title_note,priority,user_number))
            cursor.execute('''SELECT note_number FROM note WHERE user_number=?''',(user_number,))
            result=cursor.lastrowid
            return result

    def delete_note(self,note_number,user_number):
        with sqlite3.connect("database.db") as connection:
            cursor =connection.cursor()
            cursor.execute('''DELETE FROM note WHERE note_number=? AND user_number=?''',(note_number,user_number))
            return cursor.rowcount

    def get_notes(self,user_number):
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT title_note ,notes,priority FROM note WHERE user_number=? ''',(user_number,))
            return cursor.fetchall()

    def change_note(self,title_note,note_number,user_number):
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE note SET title_note=? WHERE note_number=? AND user_number=?''',(title_note,note_number,user_number))
            return cursor.rowcount

    def get_note(self,note_number,user_number):
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT  title_note ,notes FROM note WHERE note_number=? AND user_number=? ''',(note_number,user_number))
            return cursor.fetchone()