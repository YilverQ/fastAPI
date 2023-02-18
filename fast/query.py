from fastapi import FastAPI
from typing import Union

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

#Parametros query son parametros opcionales.
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
"""
    http://127.0.0.1:8000/items/?skip=0&limit=10
    http://127.0.0.1:8000/items/
    http://127.0.0.1:8000/items/?skip=20

    skip = cuantos saltos o registro ignora. 
    limit = cantidad máxima de registro en la consulta.
"""


"""
"""
#Podemos tener un query con valor por defecto.
#'Union' tenemos que importarlo de typing -> Revisar línea 2.
#'q' es un string y podemos pasarle cualquier valor. 
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


#Otra forma de definir parametros. 
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

"""El ejemplo funciona para:
    http://127.0.0.1:8000/items/foo?short=1
    http://127.0.0.1:8000/items/foo?short=True
    http://127.0.0.1:8000/items/foo?short=true
    http://127.0.0.1:8000/items/foo?short=on
    http://127.0.0.1:8000/items/foo?short=yes
"""


#Definir varios parametros de tipo Path y luego definir query.
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

"""
    No importa el orden de los parametros path. 
    El framework es inteligente y sabe cual es la posición de ambos. 
    Lo que si es importante es definir los parametros query luego de los path. 
"""


#Parametros query requeridos. 
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

"""
    Simplemente no definimos un valor por defecto. 
    En ese caso, debemos agregar un valor query. 

    Error: http://127.0.0.1:8000/items/foo-item
    Success: http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
"""


#Tambíen podemos definir parametros query con valor por defecto y query obligatorios. 
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

"""
    El framework ya conocer los valores que deben ser por defecto y los que no. 
    En este caso hay tres parametros:     
        needy, un str requerido.
        skip, un int con un valor por defecto de 0.
        limit, un int opcional.
"""