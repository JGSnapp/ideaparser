from sqlalchemy import Column, Integer, String, Date, Float, Text
from .db import Base

class TrendRaw(Base):
    __tablename__ = "trend_raw"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    keyword = Column(String, index=True)
    date = Column(Date, index=True)
    value = Column(Float)

class DailyHotTopic(Base):
    __tablename__ = "daily_hot_topics"
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True)
    trend_score = Column(Float)
    date = Column(Date, index=True)

class IdeaCard(Base):
    __tablename__ = "idea_cards"
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True)
    problem = Column(Text)
    solution = Column(Text)
    tam = Column(Text)
    why_now = Column(Text)
    next_steps = Column(Text)
    hypothesis = Column(Text, nullable=True)
