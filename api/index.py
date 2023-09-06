from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Optional
from dotenv import load_dotenv
from api.services.qabot.qabot import QABotService

load_dotenv()

app = FastAPI()


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

        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
