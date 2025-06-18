from fastapi import FastAPI, Depends, WebSocket, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import DailyHotTopic, IdeaCard
from .idea_agent import generate_idea_cards, generate_hypothesis_card
from .aggregator import compute_daily_scores
from .trending import collect_trend
from . import tasks  # start background scheduler
import asyncio

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/topics")
def read_topics(db: Session = Depends(get_db)):
    topics = db.query(DailyHotTopic).order_by(DailyHotTopic.trend_score.desc()).limit(10).all()
    return topics

@app.post("/ideas")
async def create_ideas(db: Session = Depends(get_db)):
    await asyncio.get_event_loop().run_in_executor(None, generate_idea_cards, db)
    return {"status": "processing"}


@app.post("/hypotheses")
async def create_hypothesis(description: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    def run():
        generate_hypothesis_card(db, description)
    background_tasks.add_task(run)
    return {"status": "processing"}

@app.get("/hypotheses/{card_id}")
def read_hypothesis(card_id: int, db: Session = Depends(get_db)):
    card = db.query(IdeaCard).filter(IdeaCard.id == card_id).first()
    if card:
        return card
    return JSONResponse(status_code=404, content={"detail": "Not found"})

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_text("ready")
    await ws.close()
