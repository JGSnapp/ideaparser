from datetime import date
from pytrends.request import TrendReq
import praw
import tweepy
import requests
from sqlalchemy.orm import Session
from .models import TrendRaw
from .config import (
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_SECRET,
    PRODUCTHUNT_TOKEN,
)


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


def fetch_twitter_mentions(keyword: str) -> float:
    if not all([
        TWITTER_API_KEY,
        TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_SECRET,
    ]):
        return 0.0
    try:
        auth = tweepy.OAuth1UserHandler(
            TWITTER_API_KEY,
            TWITTER_API_SECRET,
            TWITTER_ACCESS_TOKEN,
            TWITTER_ACCESS_SECRET,
        )
        api = tweepy.API(auth)
        tweets = api.search_tweets(q=keyword, count=100)
        return float(len(tweets))
    except Exception:
        return 0.0


def fetch_product_hunt_mentions(keyword: str) -> float:
    if not PRODUCTHUNT_TOKEN:
        return 0.0
    headers = {"Authorization": f"Bearer {PRODUCTHUNT_TOKEN}"}
    query = {
        "query": f"{{ search(query: \"{keyword}\", first: 20) {{ edges {{ node {{ __typename }} }} }} }}"
    }
    try:
        r = requests.post(
            "https://api.producthunt.com/v2/api/graphql", json=query, headers=headers
        )
        data = r.json()
        count = len(data.get("data", {}).get("search", {}).get("edges", []))
        return float(count)
    except Exception:
        return 0.0


def collect_trend(db: Session, keyword: str):
    gt = fetch_google_trends(keyword)
    rd = fetch_reddit_mentions(keyword)
    tw = None
    if all([
        TWITTER_API_KEY,
        TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_SECRET,
    ]):
        tw = fetch_twitter_mentions(keyword)

    ph = None
    if PRODUCTHUNT_TOKEN:
        ph = fetch_product_hunt_mentions(keyword)
    today = date.today()
    db.add(TrendRaw(source='google_trends', keyword=keyword, date=today, value=gt))
    db.add(TrendRaw(source='reddit', keyword=keyword, date=today, value=rd))
    if tw is not None:
        db.add(TrendRaw(source='twitter', keyword=keyword, date=today, value=tw))
    if ph is not None:
        db.add(
            TrendRaw(source='producthunt', keyword=keyword, date=today, value=ph)
        )
    db.commit()
