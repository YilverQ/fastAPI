from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


basic_auth = APIRouter()


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


users_db = {
	'mouredev' : {
		'username'  : 'mouredev',
		'fullname'  : 'Brais Moure',
		'email' 	: 'moure@gmail.com',
		'disabled'  : False,
		'password'  : '123456'
	},
	'mouredev2' : {
		'username'  : 'mouredev',
		'fullname'  : 'Brais Moure 2',
		'email' 	: 'brais@gmail.com',
		'disabled'  : True,
		'password'  : '456789'
	},
	'yilver' : {
		'username'  : 'yilver',
		'fullname'  : 'Yilver Quevedo',
		'email' 	: 'yilver@gmail.com',
		'disabled'  : False,
		'password'  : 'root'
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



async def current_user(token : str = Depends(oath2)):
	user = search_user(token)
	if not user:
		raise HTTPException(
			status_code = status.HTTP_401_UNAUTHORIZED, 
			detail 		= 'You not have authrorized!',
			headers 	= {'WWW-Authenticate' : 'Bearer'})

	if user.disabled:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST, 
			detail = 'Sorry, your user are disabled!')

	return user


#Depends : Va a recibir datos pero no depende de nadie 'Depends()'.
@basic_auth.post('/login')
async def login(form : OAuth2PasswordRequestForm = Depends()):
	user_db = users_db.get(form.username)
	if not user_db:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST, 
			detail='The username is not correct!')

	user = search_user_db(form.username)

	if not user.password == form.password:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST, 
			detail='The password is not correct!')

	return {'access_token' : user.username, 'token_type' : 'Bearer'} 


@basic_auth.get('/users/me')
async def me(user : User = Depends(current_user)):
	return user