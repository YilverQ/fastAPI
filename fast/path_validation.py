from fastapi import FastAPI, Path, Query

app = FastAPI()


#También podemos agregar validación a los parametros que vienen en el path.
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: str | None = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


#Podemos definir el orden de los parámetros.
#Para ello tenemos que pasar primero el valor de *.
#Python no hace nada con ello, pero le dará a entender que vamos a pasar varios parámetros en un orden que nosotros definamos. 
@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


#Validación de número. (Igual a 1 o mayor)
@app.get("/items/{item_id}")
async def read_items(
    *, item_id: int = Path(title="The ID of the item to get", ge=1), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
"""
    Aquí, con ge=1, item_id deberá ser un número entero "mayor o igual" a 1
"""


#De igual modo podemos definir un número menor a '1000'
@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
"""
    gt: mayor que
    le: menor o igual
"""



#Validación para número flotantes.
@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(gt=0, lt=10.5)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

"""
    gt: mayor que
    ge: mayor o igual
    lt: menos que
    le: menor o igual
"""