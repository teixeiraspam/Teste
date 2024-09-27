from fastapi import FastAPI
import uvicorn
from setuptools import wheel

app = FastAPI()

@app.get("/example")

def example():
    return {"message": "Hello API"}


if __name__== "__main__":
    uvicorn.run (app, port=8000)


