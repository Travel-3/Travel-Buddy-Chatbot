from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from dotenv import load_dotenv
from api.services.qabot.qabot import QABotService

load_dotenv()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "*",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}


@app.get('/api/events/qa')
def eventsQA(query: Optional[str] = None):
    try:
        res = QABotService.qaEvent(query)
        return {'status': True, 'content': res}
    except Exception as e:
        return JSONResponse(content={'status': False, 'message': str(e)}, status_code=500)


@app.get('/api/events/qa/steaming', response_class=StreamingResponse)
def eventsQAStreaming(query: Optional[str] = None):
    try:
        # You can directly return a generator in FastAPI for streaming
        def generate():
            for line in QABotService.qaEventStreaming(query):
                # Assuming each line is a string and you can directly yield it
                yield line

        return StreamingResponse(generate(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "Content-Type": "text/event-stream"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
