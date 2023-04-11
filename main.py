from fastapi import FastAPI
from pydantic import BaseModel

from core.app import Generate_summary

class Inputs(BaseModel):
    url: str
    keyword: str

app = FastAPI()


@app.get("/test")
async def root():
    return {"message":"Hello World"}

@app.post("/generate")
async def generate(inputs: Inputs):
    return Generate_summary(inputs.url,inputs.keyword)