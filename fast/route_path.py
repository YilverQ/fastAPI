from fastapi import FastAPI

app = FastAPI()


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

"""
    Podrías necesitar que el parámetro contenga /home/johndoe/myfile.txt con un slash inicial (/).

    En este caso la URL sería /files//home/johndoe/myfile.txt con un slash doble (//) entre files y home.
"""