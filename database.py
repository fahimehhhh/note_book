import sqlite3
import os
class Database():
    def __init__(self):
        self.create_table()
        
    def create_table(self):
        with sqlite3.connect("database.db") as connection:
            cursor=connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users 
            (user_names TEXT UNIQUE NOT NULL,password_users TEXT NOT NULL ,user_number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, token_users TEXT UNIQUE )''')
         
            cursor.execute('''CREATE TABLE IF NOT EXISTS note
            (note_number INTEGER PRIMARY KEY AUTOINCREMENT,notes TEXT NOT NULL ,title_note TEXT NOT NULL ,create_at NOT NULL ,user_number INTEGER ,FOREIGN KEY(user_number)  REFERENCES users(user_number))''')

    
    def get_user_number(self,token_user):
        with sqlite3.connect('database.db') as connection:
            cursor=connection.cursor()
            cursor.execute('''SELECT user_number FROM users WHERE token_users=?''',(token_user,))
            print(repr(f'token user {token_user}'))
            result=cursor.fetchone()
            print(f"result{result}")
            return result
       


    def register(self,user_names,password_users):
        with sqlite3.connect("database.db") as connection:
            cursor =connection.cursor()
            cursor.execute('''INSERT INTO users (user_names,password_users) VALUES(?,?)''',(user_names,password_users))
            return cursor.lastrowid

    def login(self,token_user ,user_names):
        with sqlite3.connect("database.db") as connection:
            cursor =connection.cursor()
            cursor.execute('''UPDATE  users SET token_users=?  WHERE user_names=?''',(token_user,user_names))
            cursor.execute('''SELECT token_users FROM users WHERE user_names=?''',(user_names,))
            return cursor.fetchone()
           



    def check_username(self,user_name,password_user):
        with sqlite3.connect("database.db") as connection:
            cursor=connection.cursor()
            cursor.execute('''SELECT user_names,password_users FROM users WHERE (user_names,password_users)=(?,?)''',(user_name,password_user))
            return cursor.fetchone()

    def get_users(self):
        with sqlite3.connect("database.db") as connection:
            cursor=connection.cursor()
            cursor.execute('''SELECT user_names,password_users,token_users FROM users''')
            result=cursor.fetchall()
            print(repr(result))
            return result
    def insert_note(self,notes,title_note,user_number):
        with sqlite3.connect("database.db") as connection:
            cursor=connection.cursor()
            cursor.execute('''INSERT INTO note (notes,title_note,user_number,create_at)  VALUES(?,?,?,0)''',(notes,title_note,user_number))
            return cursor.lastrowid

    def delete_note(self,note_number,user_number):
        with sqlite3.connect("database.db") as connection:
            cursor =connection.cursor()
            cursor.execute('''DELETE FROM note WHERE note_number=? AND user_number=?''',(note_number,user_number))
            return cursor.rowcount

    def get_notes(self,user_number):
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT title_note FROM note WHERE user_number=? ''',(user_number,))
            return cursor.fetchall()

    def change_note(self,title_note,note_number,user_number):
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE note SET title_note=? WHERE note_number=? AND user_number=?''',(title_note,note_number,user_number))
            return cursor.rowcount
    

    def get_note(self,note_number,user_number):
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT  title_note FROM note WHERE note_number=? AND user_number=? ''',(note_number,user_number))
            return cursor.fetchone()