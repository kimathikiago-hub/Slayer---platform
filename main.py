from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from engine import DerivEngine

app = FastAPI()
engine = DerivEngine()

# This allows your website to talk to your server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(engine.connect())

@app.get("/live-data")
async def get_data():
    return {
        "signal": engine.signal,
        "neglect": engine.neglect_counts,
        "history": engine.digits_history[-10:]
    }
