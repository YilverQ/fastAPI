from fastapi import FastAPI
from pydantic import BaseModel

#Estructura de nuestro dato. Usa Pydantic
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()

#No hace falta especificarlo en la ruta.
#Los datos se envían a traves del body request.
@app.post("/items/")
async def create_item(item: Item):
    #Convertimos de un dato tipo Pydantic a un diccionario.
    item_dict = item.dict()
    if item.tax:
        #Podemos acceder a todos los atributos del modelo.
        #'método update sirve para actualizar el diccionario'
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


#Podemos declarar parámetros de ruta y cuerpo de la solicitud al mismo tiempo. 
#Al final convertimos el modelo a un diccionario para que pueda ser entendido como JSON.
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


#También podemos declarar query al mismo tiempo
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result