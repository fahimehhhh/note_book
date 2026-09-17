from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from database import Database
app = FastAPI()

class Note(BaseModel):
    title:str
    note:str

class Change_note(BaseModel):
    title:str

class User(BaseModel):
    user_name:str
    user_password:int



@app.post("/register")
def register(user:User):
    
    db=Database()
    user_name = user.user_name.strip()
    if user_name =='':
        raise(HTTPException(422,'unprocessable content'))

    elif user_name.__len__() >20:
        raise(HTTPException(422,'unprocessable content'))

    if  db.check_username(user_name) == []:
        db.register(user.user_name,user.user_password)
        return ('user retisted')
    else:
        raise(HTTPException(409,'conflict'))

@app.post("/new note")
def new_note (note:Note):
    db=Database()
    title =note.title.strip(' ')
    if title =='':
        raise HTTPException(400,'Bad Request')
    count =title.__len__()
    if count > 20 :
        raise HTTPException(400,'bad request')
    
    note_number=db.insert_note(note.note,title)
    return (f"A Not Title {title.capitalize()} Was Added with number {note_number}")


@app.delete("/note")
def delete_note(note_number:int):
    db=Database()
    deleted=db.delete_note(note_number)
    if deleted:
       return (f"A Not Title {note_number} Was Deleted")
    
    return ('the operation failed')


@app.get("/my notes")
def get_notes():
    db=Database()
    title_note =db.get_notes()
    return title_note

@app.put("/change_note")
def change_note(note:Change_note,note_number:int):
    title_note=note.title
    db=Database()
    db.change_note(title_note,note_number)

@app.get("/search_note")
def search_note(note_number:int):
    db=Database()
    title_note=db.get_note(note_number)
    return title_note
