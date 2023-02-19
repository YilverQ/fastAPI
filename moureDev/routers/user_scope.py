from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

user = APIRouter(prefix='/user',
                 tags = ['User'])

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
@user.post('/', status_code=201)
async def create(user : User):
    if type(search_user(user.id_key)) == User:
        raise HTTPException(status_code = 202, detail='User already exist!')
    users_db.append(user)
    result = {'detail' : 'Users has created!'}
    result.update({'user' : user.dict()})
    return result


#Read all users
@user.get('/all')
async def read_all():
    return users_db


#Read only one user.
@user.get('/{id_user}')
async def read(id_user : int):
    if search_user(id_user):
        return search_user(id_user)
    raise HTTPException(status_code = 404, detail='User not found!')


#Update one user. 
@user.put('/')
async def update(user : User):
    for index, item in enumerate(users_db):
        if item.id_key == user.id_key:
            users_db[index] = user
            return user
    raise HTTPException(status_code = 404, detail='User not found!')


#Delete one user.
@user.delete('/{id_user}')
async def delete(id_user : int):
    for index, item in enumerate(users_db):
        if item.id_key == id_user:
            # users_db.pop(index)
            del users_db[index]
            return {'detail' : 'User has deleted!'}
    raise HTTPException(status_code = 404, detail='User not found!')


def search_user(id_user : int):
    #users = ((x for x in users_db if x.id_key == id_user), None)
    user = list(filter(lambda user: user.id_key == id_user, users_db))
    try:
        return user[0]
    except:
        return False