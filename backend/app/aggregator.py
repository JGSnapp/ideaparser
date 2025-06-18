from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import TrendRaw, DailyHotTopic


def compute_daily_scores(db: Session):
    today = date.today()
    results = (
        db.query(TrendRaw.keyword, func.sum(TrendRaw.value).label('score'))
        .filter(TrendRaw.date == today)
        .group_by(TrendRaw.keyword)
        .all()
    )
    for keyword, score in results:
        db.add(DailyHotTopic(keyword=keyword, trend_score=score, date=today))
    db.commit()
