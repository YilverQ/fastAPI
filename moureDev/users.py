from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#Model
class User(BaseModel):
    id_key   : int
    name     : str
    lastname : str
    email    : str
    age      : int 

#Data type 'User'
users_db = [User(id_key = 1, name = "Yilver", lastname = "Quevedo", email = "yilver@gmail.com", age = 21),
            User(id_key = 2, name = "Biagni", lastname = "Abano", email = "biangi@gmail.com", age = 21),
            User(id_key = 3, name = "Sebastían", lastname = "Martínez", email = "sabastian@gmail.com", age = 10),
            User(id_key = 4, name = "Michelle", lastname = "Rodríguez", email = "michelle@gmail.com", age = 26)
]


#Create user
@app.post('/user')
async def create(user : User):
    if type(search_user(user.id_key)) == User:
        return {'error' : 'User already exist!'}
    users_db.append(user)
    return users_db


#Read all users
@app.get('/users')
async def read_all():
    return users_db


#Read only one user.
@app.get('/user/{id_user}')
async def read(id_user : int):
    return search_user(id_user)


#Update one user. 
@app.put('/user')
async def update(user : User):
    for index, item in enumerate(users_db):
        if item.id_key == user.id_key:
            users_db[index] = user
            return user
    return {'error' : 'No se ha encontrado el usuario'}


#Delete one user.
@app.delete('/user/{id_user}')
async def delete(id_user : int):
    for index, item in enumerate(users_db):
        if item.id_key == id_user:
            # users_db.pop(index)
            del users_db[index]
            return {'message' : 'User has deleted!'}
    return {'error' : 'No se ha encontrado el usuario'}


def search_user(id_user : int):
    #users = ((x for x in users_db if x.id_key == id_user), None)
    user = list(filter(lambda user: user.id_key == id_user, users_db))
    try:
        return user[0]
    except:
        return {'error' : 'No se ha encontrado el usuario'}