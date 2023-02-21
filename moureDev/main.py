from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import user, product, basic_auth, jwt_auth


#Instanciamos FastAPI
app = FastAPI()

#Incluimos todas las rutas.
app.include_router(user)
app.include_router(product)

#app.include_router(basic_auth)
app.include_router(jwt_auth)

#Incluimos los archivos estáticos.
app.mount('/static', StaticFiles(directory='static'), name='static')

#Rutas
@app.get('/')
async def root():
    return {'detail'    : 'Home page',
            'message'   : 'Hello world from FastApi',
            'API doc'   : 'localhost:8000/docs',
            'redoc'     : 'localhost:8000/redoc',
            'JsonAPI'   : 'localhost:8000/openapi.json'}

