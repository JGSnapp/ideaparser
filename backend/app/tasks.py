from apscheduler.schedulers.background import BackgroundScheduler
from .db import SessionLocal
from .trending import collect_trend
from .aggregator import compute_daily_scores

KEYWORDS = ["AI", "Blockchain", "Startup"]

scheduler = BackgroundScheduler()

def collect_job():
    db = SessionLocal()
    for kw in KEYWORDS:
        collect_trend(db, kw)
    db.close()

def aggregate_job():
    db = SessionLocal()
    compute_daily_scores(db)
    db.close()

scheduler.add_job(collect_job, 'interval', hours=6)
scheduler.add_job(aggregate_job, 'cron', hour=0)

scheduler.start()
