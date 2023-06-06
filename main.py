import asyncio
import json

from fastapi import FastAPI, Request, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

STREAM_DELAY = 20  # milliseconds
RETRY_TIMEOUT = 15000  # milliseconds

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

@app.get("/generate")
async def generate(request: Request, url: str = Query(...), keyword: str = Query(...)):
    async def event_generator():
        output = Generate_summary(url, keyword)
        for chunk in output:
            if await request.is_disconnected():
                break

            yield json.dumps(chunk)

            # Wait for a time before sending the next chunk.
            await asyncio.sleep(STREAM_DELAY / 1000)

    return EventSourceResponse(event_generator())

@app.get('/test-stream')
async def message_stream(request: Request):
    def new_messages():
        # Add logic here to check for new messages
        yield 'Hello World'

    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_messages():
                yield {
                        "event": "new_message",
                        "id": "message_id",
                        "retry": RETRY_TIMEOUT,
                        "data": "message_content"
                }

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())
