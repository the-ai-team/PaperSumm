from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from core.app import Generate_summary

class Inputs(BaseModel):
    url: str
    keyword: str

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
async def root():
    return {"message":"Hello World"}

@app.post("/generate")
async def generate(inputs: Inputs):
    return Generate_summary(inputs.url,inputs.keyword)