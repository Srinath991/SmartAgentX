from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List
from ..agents.assistant import create_agent
from ..config.settings import get_settings
import os

app = FastAPI(title="Smart Agent X", description="Multi-Tool AI Assistant")
settings = get_settings()

# Set up templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "../templates"))

class Query(BaseModel):
    text: str
    chat_history: Optional[List[dict]] = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query")
async def process_query(query: Query):
    try:
        agent = create_agent()
        response = await agent.ainvoke({
            "input": query.text,
            "chat_history": query.chat_history
        })
        return {"response": response["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": settings.MODEL_NAME} 