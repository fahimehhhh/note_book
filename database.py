import sqlite3

class Database():
    def __init__(self):
        self.connection=sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.create_table()
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
        (user_names TEXT UNIQUE NOT NULL,password_users TEXT NOT NULL ,user_number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL  )''')
         
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS note
        (note_number INTEGER PRIMARY KEY AUTOINCREMENT,notes TEXT NOT NULL ,title_note TEXT NOT NULL ,create_at NOT NULL ,user_number INTEGER ,FOREIGN KEY(user_number)  REFERENCES users(user_number))''')

    def login_user(self,user_names,password_users):
        self.cursor.execute('''INSERT INTO users (user_names,password_users) VALUES(?,?)''',(user_names,password_users))
        return True

   
    def insert_note(self,notes,title_note):
        self.cursor.execute('''INSERT INTO note (notes,title_note,create_at)  VALUES(?,?,0)''',(notes,title_note))
        self.connection.commit()
        return self.cursor.lastrowid

    def delete_note(self,note_number):
        self.cursor.execute('''DELETE FROM note WHERE note_number=?''',(note_number,))
        self.connection.commit()
        return True

    def get_notes(self):
        self.cursor.execute('''SELECT title_note FROM note ''')
        return self.cursor.fetchall()

    def change_note(self,title_note,note_number):
        self.cursor.execute('''UPDATE note SET title_note=? WHERE note_number=?''',(title_note,note_number))
        self.connection.commit()
    

    def get_note(self,note_number):
        self.cursor.execute('''SELECT  title_note FROM note WHERE note_number=?''',(note_number,))
        return self.cursor.fetchone()