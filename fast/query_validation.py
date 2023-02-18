from fastapi import FastAPI, Query

app = FastAPI()

#Definimos que 'q' es opcional.
#Pero también comprobamos que tenga un máximo de 50 caracteres.
@app.get("/items/")
async def read_items(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


#Podemos agregar más validaciones.
@app.get("/items/")
async def read_items(q: str | None = Query(default=None, min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


#Incluso podemos agregar expresiones regulares. 
@app.get("/items/")
async def read_items(
    q: str
    | None = Query(default=None, min_length=3, max_length=50, regex="^fixedquery$")
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


#Así definimos un parametro query requerido y con validación. 
@app.get("/items/")
async def read_items(q: str = Query(min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



#Otra forma de definir parámetros requeridos de tipo query es así.
#Importamos 'Required' de Pydantic.
from pydantic import Required
@app.get("/items/")
async def read_items(q: str = Query(default=Required, min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


#Para definir multiples parámetros. 
@app.get("/items/")
async def read_items(q: list[str] | None = Query(default=None)):
    query_items = {"q": q}
    return query_items

"""
    http://localhost:8000/items/?q=foo&q=bar

    Response:
        {
          "q": [
            "foo",
            "bar"
          ]
        }

    Para declarar un parámetro de consulta con un tipo de lista, como en el ejemplo anterior, 
    debe usar Query explícitamente; de lo contrario, se interpretaría como un cuerpo de solicitud.
"""


#Definir multiples parámetros con valor por defecto. 
@app.get("/items/")
async def read_items(q: list[str] = Query(default=["foo", "bar"])):
    query_items = {"q": q}
    return query_items

#definimos un parámetro de tipo lista con valor vacío. 
@app.get("/items/")
async def read_items(q: list = Query(default=[])):
    query_items = {"q": q}
    return query_items



#Podemos declarar más información. 
#En el ejemplo podemos ver que agregamos dos metainformación. (title y descrition)
@app.get("/items/")
async def read_items(
    q: str
    | None = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



#Podemos definir alias para los parámetros. 
#tenemos que: 
"""
    http://127.0.0.1:8000/items/?item-query=foobaritems
    Dónde 'item-query' es nuestro parámetro.
    Pero como 'item-query' no es una sentencia valida para python.
    Podemos hacer lo siguiente. 

"""
@app.get("/items/")
async def read_items(q: str | None = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



#Valores obsoletos. 
#Con esto indicamos que la ruta está obsoleta. 
#En este caso sigue funcionando la ruta pero no se está actualizando. 
@app.get("/items/")
async def read_items(
    q: str
    | None = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



#Excluir de OpenAPI
@app.get("/items/")
async def read_items(
    hidden_query: str | None = Query(default=None, include_in_schema=False)
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}