from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel
from database import Database
from pwdlib import PasswordHash
from typing import Literal
import secrets


password_hash=PasswordHash.recommended()
app = FastAPI()

class Note(BaseModel):
    title:str
    note:str
    priority:Literal['low', 'medium','high']

class Change_note(BaseModel):
    title:str

class User(BaseModel):
    user_name:str
    user_password:str

httpbearer =HTTPBearer()


def get_current_user(token:HTTPAuthorizationCredentials = Depends(httpbearer) ):
    token =token.credentials.strip('""')
    db=Database()
    user_number=db.get_user_number(token)
    print(user_number)
    if user_number is None:
        raise (HTTPException(401,'invalid token'))
    else:
        user_number=user_number[0]
        return user_number
    
@app.get('/')
def get():
    return FileResponse('frontend.html')

@app.get('/style.css')
def style():
    return FileResponse('style.css')

@app.get('/test')
def test(authorization:HTTPAuthorizationCredentials= Depends(httpbearer)):
    return authorization.credentials

@app.post("/register")
def register(user:User):
    db=Database()
    password_hashing=password_hash.hash(user.user_password)
    user_name = user.user_name.strip()
    if user_name =='':
        raise(HTTPException(422,'unprocessable content'))
    elif user_name.__len__() >20:
        raise(HTTPException(422,'unprocessable content'))
    if  db.check_username(user_name) is None:
        db.register(user_name,password_hashing)
        return (f'user registed and user_name is {user_name}')
    else:
        raise(HTTPException(409,'conflict'))

@app.post("/login")
def login(user:User):
    password=user.user_password
    token_user =secrets.token_urlsafe()
    user_name =user.user_name
    db=Database()
    result =db.check_username(user_name)
    if result != None:
       password_stored=db.check_password(user_name)
       password_stored=password_stored[0]
       if password_hash.verify(password,password_stored):
            token =db.login(token_user,user_name)
            return token[0]
       else:
            raise(HTTPException(409,'conflict'))
    else:
        raise(HTTPException(400,'badRequest'))
@app.post("/new_note")
def new_note (note:Note,user_number:int=Depends(get_current_user)):
    db=Database()
    title =note.title.strip(' ')
    if title =='':
        raise HTTPException(422,'unprocessable content')
    count =title.__len__()
    if count > 20 :
        raise HTTPException(422,'unprocessable content')
    note_number=db.insert_note(note.note,title,note.priority,user_number)
    return (f"A Not Title {title.capitalize()} Was Added with number {note_number}")


@app.delete("/delete_note")
def delete_note(note_number:int,user_number:int= Depends(get_current_user)):
    db=Database()
    deleted=db.delete_note(note_number,user_number)
    if deleted==1:
       return (f"A Note number {note_number} Was Deleted")
    else:
        raise (HTTPException(400,'bad_request'))


@app.get("/my_notes")
def get_notes(user_number:int=Depends(get_current_user)):
    db=Database()
    title_note =db.get_notes(user_number)
    if title_note ==[]:
        raise(HTTPException(400,'bad request'))
    return title_note
@app.put("/change_note")
def change_note(note:Change_note,note_number:int,user_number:int=Depends(get_current_user)):
    title_note=note.title
    db=Database()
    result =db.change_note(title_note,note_number,user_number)
    if result == 1:
        return ('sucssesfully')
    raise(HTTPException(400,'bad request'))

@app.get("/search_note")
def search_note(note_number:int,user_number:int=Depends(get_current_user)):
    db=Database()
    title_note=db.get_note(note_number,user_number)
    print(title_note)
    if title_note is None:
        raise(HTTPException(404,'not found'))

    else:
        title=title_note[0]
        note=title_note[1]
        return (f'title:{title},note:{note}')
