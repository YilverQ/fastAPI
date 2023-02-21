#Librerías e importaciones
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITH = 'HS256'
ACCESS_TOKEN_DURATION = 1
crypt = CryptContext(schemes=['bcrypt'])
SECRET_KEY = '2663dd50256657fc08224dd70e0a2b8348a51c1eee4a0c4147bf8988f7e52ec8'

jwt_auth = APIRouter()


#Criterio de autenticación
#Le pasamos la ruta encargada de hacer la autenticación.
oath2 = OAuth2PasswordBearer(tokenUrl = 'login')


#Modelo User, es lo que se va a pasar al front-end.
class User(BaseModel):
	username : str
	fullname : str
	email 	 : str
	disabled : bool

#Heredamos de User y añadimos un valor adicional 'password'.
class UserDB(User):
	password : str


#Base de datos
users_db = {
	'mouredev' : {
		'username'  : 'mouredev',
		'fullname'  : 'Brais Moure',
		'email' 	: 'moure@gmail.com',
		'disabled'  : False,
		'password'  : '$2a$12$YH2CEoFpn7K6OEMjRmyPeeGKVwV0eTtyeaHDSv25p7HzUHqHM3DJq'
	},
	'mouredev2' : {
		'username'  : 'mouredev',
		'fullname'  : 'Brais Moure 2',
		'email' 	: 'brais@gmail.com',
		'disabled'  : True,
		'password'  : '$2a$12$UMzcHCjATtrdgGCq4TkTYetay9FmKHxnUkl.Ljv80s79rXOmz/9b.'
	},
	'yilver' : {
		'username'  : 'yilver',
		'fullname'  : 'Yilver Quevedo',
		'email' 	: 'yilver@gmail.com',
		'disabled'  : False,
		'password'  : '$2a$12$XsT1L05HXhxBwVzFlZm2xOPdyNtc7uA7ch/V/QSxPlz11HQ1QnXdy'
	}
}

#Buscamos un usuario en la base de datos
def search_user_db(username : str):
	if username in users_db:
		return UserDB(**users_db[username])
		"""
			esto:
				UserDB(**users_db[username]) 
			es igual a decir:
				UserDB(username:users_db[username]['username'], etc)
		"""
		
def search_user(username : str):
	if username in users_db:
		return User(**users_db[username])

async def auth_user(token: str = Depends(oath2)):
	exception = HTTPException(
					status_code = status.HTTP_401_UNAUTHORIZED, 
					detail 		= 'You not have authrorized!',
					headers 	= {'WWW-Authenticate' : 'Bearer'})
	
	try:
		username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITH]).get('sub')
		if username is None:
			raise exception


	except JWTError:
		raise exception
	
	return search_user(username)


async def current_user(user : User = Depends(auth_user)):
	if user.disabled:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST, 
			detail = 'Sorry, your user are disabled!')

	return user

#Depends : Va a recibir datos pero no depende de nadie 'Depends()'.
@jwt_auth.post('/login')
async def login(form : OAuth2PasswordRequestForm = Depends()):
	user_db = users_db.get(form.username)
	if not user_db:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST, 
			detail='The username is not correct!')

	user = search_user_db(form.username)

	if not crypt.verify(form.password, user.password):
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST, 
			detail='The password is not correct!')

	access_token = {'sub' : user.username, 
		 			'exp' : datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

	jwt_encode = jwt.encode(access_token, 
			 				SECRET_KEY, 
							algorithm=ALGORITH)

	return {'access_token' : jwt_encode,
	 		'token_type' : 'Bearer'} 


@jwt_auth.get('/users/me')
async def me(user : User = Depends(current_user)):
	return user