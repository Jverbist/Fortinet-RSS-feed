import asyncio
import feedparser
import hashlib
import logging
from .email import send_email
from .tracker import get_new_posts

logger = logging.getLogger(__name__)

FEEDS = [
    "https://support.fortinet.com/rss/csb.xml",
]

def get_color_from_id(bulletin_id: str) -> str:
    """Generate a consistent hex color from bulletin ID"""
    hash_obj = hashlib.md5(bulletin_id.encode())
    hash_hex = hash_obj.hexdigest()[:6]
    return f"#{hash_hex}"

async def fetch_feeds():
    loop = asyncio.get_event_loop()
    results = await asyncio.gather(*(loop.run_in_executor(None, feedparser.parse, url) for url in FEEDS))
    formatted = []
    for url, feed in zip(FEEDS, results):
        entries = []
        for e in feed.entries[:10]:
            # Extract bulletin ID from title (e.g., "CSB-260320-1 updated: ...")
            title = e.get("title", "")
            bulletin_id = title.split(" ")[0] if title else "CSB"
            color = get_color_from_id(bulletin_id)
            
            entries.append({
                "title": title,
                "link": e.get("link", ""),
                "published": e.get("published", ""),
                "bulletin_id": bulletin_id,
                "color": color,
                "id": e.get("id", title)
            })
        
        formatted.append({
            "title": feed.feed.get("title", url),
            "link": feed.feed.get("link", ""),
            "entries": entries
        })
    return formatted

async def check_for_new_posts():
    """Check for new posts and send email notifications"""
    try:
        feeds = await fetch_feeds()
        
        for feed in feeds:
            new_posts = get_new_posts(feed["entries"])
            
            for post in new_posts:
                logger.info(f"New post detected: {post['bulletin_id']}")
                await send_email(
                    subject=f"🔔 New Fortinet Security Bulletin: {post['bulletin_id']}",
                    bulletin_id=post['bulletin_id'],
                    title=post['title'],
                    link=post['link'],
                    published=post['published'],
                    color=post['color']
                )
    except Exception as e:
        logger.error(f"Error checking for new posts: {e}")

