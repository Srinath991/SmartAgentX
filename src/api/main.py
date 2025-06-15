from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ..agents.assistant import create_agent
from ..config.settings import get_settings

app = FastAPI(title="Smart Agent X", description="Multi-Tool AI Assistant")
settings = get_settings()
agent = create_agent()

class Query(BaseModel):
    text: str

@app.post("/query")
async def process_query(query: Query):
    try:
        response = await agent.ainvoke({
            "input": query.text,
        })
        return {"response": response["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": settings.MODEL_NAME} 