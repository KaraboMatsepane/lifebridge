from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"name": "Karabo",
            "age": 25
            }