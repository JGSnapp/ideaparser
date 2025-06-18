from datetime import date
from pytrends.request import TrendReq
import praw
from sqlalchemy.orm import Session
from .models import TrendRaw

# Placeholder functions for Twitter/X and Product Hunt

def fetch_google_trends(keyword: str) -> float:
    pytrend = TrendReq()
    pytrend.build_payload([keyword])
    data = pytrend.interest_over_time()
    if not data.empty:
        return float(data[keyword].iloc[-1])
    return 0.0

def fetch_reddit_mentions(keyword: str) -> float:
    reddit = praw.Reddit(client_id='dummy', client_secret='dummy', user_agent='trend_collector')
    count = sum(1 for _ in reddit.subreddit('all').search(keyword, limit=100))
    return float(count)

# TODO: implement twitter_x_mentions and product_hunt_mentions

def collect_trend(db: Session, keyword: str):
    gt = fetch_google_trends(keyword)
    rd = fetch_reddit_mentions(keyword)
    today = date.today()
    db.add(TrendRaw(source='google_trends', keyword=keyword, date=today, value=gt))
    db.add(TrendRaw(source='reddit', keyword=keyword, date=today, value=rd))
    db.commit()
