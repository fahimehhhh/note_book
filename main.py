from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel
from database import Database
import secrets


app = FastAPI()

class Note(BaseModel):
    title:str
    note:str

class Change_note(BaseModel):
    title:str

class User(BaseModel):
    user_name:str
    user_password:str

httpbearer =HTTPBearer()

@app.get('/oo')
def get_user():
    db=Database()
    result = db.get_users()
    print(result)
    return result

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

@app.get('/test')
def test(authorization:HTTPAuthorizationCredentials= Depends(httpbearer)):
    return authorization.credentials

@app.post("/register")
def register(user:User):
    db=Database()
    user_name = user.user_name.strip()
    if user_name =='':
        raise(HTTPException(422,'unprocessable content'))
    elif user_name.__len__() >20:
        raise(HTTPException(422,'unprocessable content'))
    if  db.check_username(user_name,user.user_password) is None:
        user_number=db.register(user_name,user.user_password)
        return (f'user registed and user_number is {user_number}')
    else:
        raise(HTTPException(409,'conflict'))

@app.post("/login")
def login(user:User):
    token_user =secrets.token_urlsafe()
    user_name =user.user_name
    user_password =user.user_password
    db=Database()
    result =db.check_username(user_name,user_password)
    if result != None:
       token =db.login(token_user,user_name)
       return token[0]
        
    else:
        raise(HTTPException(400,'bad request'))
    
@app.post("/new note")
def new_note (note:Note,user_number:int=Depends(get_current_user)):
    db=Database()
    title =note.title.strip(' ')
    if title =='':
        raise HTTPException(400,'Bad Request')
    count =title.__len__()
    if count > 20 :
        raise HTTPException(400,'bad request')
    db.insert_note(note,title,user_number)
    return (f"A Not Title {title.capitalize()} Was Added with number {user_number}")


@app.delete("/delete_note")
def delete_note(note_number:int,user_number:int= Depends(get_current_user)):
    db=Database()
    deleted=db.delete_note(note_number,user_number)
    if deleted==1:
       return (f"A Note number {note_number} Was Deleted")
    else:
        raise (HTTPException(400,'bad_request'))


@app.get("/my notes")
def get_notes(user_number:int=Depends(get_current_user)):
    db=Database()
    title_note =db.get_notes(user_number)
    if title_note ==[]:
        raise(HTTPException(400,'bad request'))
    return ('sucssesfully')

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
    if title_note ==():
        raise(HTTPException(404,'not found'))
    return title_note
