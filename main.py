from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi import Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel
from database import Database
import secrets


html = '''<!DOCTYPE html>
    <html>
    <head>
    <title>test</title>
    </head>
    <body>
    <input id=user_name>
    <input id=user_password>
    <script>
    let user={user_name:document.getElementById('user_name').value,user_password:document.getElementById('user_password').value}
    let data =JSON.stringify(user)
    fetch('/login',{method:'POST',body:data,headers:{'Content-Type':'application/json'}}).then(function(response){return response.text()}).then(function(token){fetch('/test',{method:'GET',headers:{'Authorization':token}}).then(function(response){return response.text()}).then(console.log)})
    </script>
    </body>
    </html>'''


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


@app.get('/',response_class=HTMLResponse)
def get():
    return html


def get_current_user(token:HTTPAuthorizationCredentials = Depends(httpbearer) ):
    token =token.credentials
    db=Database()
    user_number=db.get_user_number(token)
    if user_number == None:
        raise (HTTPException(400,'bad request'))
    else:
        user_number=user_number[0]
        return user_number


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
    if  db.check_username(user_name,user.user_password)== []:
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


@app.get('/get_users')
def get_users():
    db=Database()
    return db.get_users()
    


@app.post("/new note")
def new_note (note:Note,note_number:int):
    db=Database()
    title =note.title.strip(' ')
    if title =='':
        raise HTTPException(400,'Bad Request')
    count =title.__len__()
    if count > 20 :
        raise HTTPException(400,'bad request')
    
    note_number=db.insert_note(note.note,title,note_number)
    return (f"A Not Title {title.capitalize()} Was Added with number {note_number}")


@app.delete("/note")
def delete_note(note_number:int,user_number:int):
    db=Database()
    deleted=db.delete_note(note_number,user_number)
    if deleted==1:
       return (f"A Note number {note_number} Was Deleted")
    else:
        raise (HTTPException(400,'bad_request'))


@app.get("/my notes")
def get_notes(user_number:int):
    db=Database()
    title_note =db.get_notes(user_number)
    if title_note ==[]:
        raise(HTTPException(400,'bad request'))
    return ('sucssesfully')

@app.put("/change_note")
def change_note(note:Change_note,note_number:int,user_number:int):
    title_note=note.title
    db=Database()
    result =db.change_note(title_note,note_number,user_number)
    if result == 1:
        return ('sucssesfully')
    raise(HTTPException(400,'bad request'))

@app.get("/search_note")
def search_note(note_number:int,user_number:int):
    db=Database()
    title_note=db.get_note(note_number,user_number)
    if title_note ==():
        raise(HTTPException(404,'not found'))
    return title_note
