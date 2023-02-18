from enum import Enum

from fastapi import FastAPI

#Definimos una clase de tipo Enum. 
#La clase tendrá 3 tipos de datos válidos.
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

#La ruta recibe un parametro. 
#Solo es valido si es valor está dentro del Enum.
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}