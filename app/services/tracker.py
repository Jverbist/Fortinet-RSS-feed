import json
import os
from pathlib import Path

TRACKER_FILE = Path(__file__).parent.parent.parent / "seen_posts.json"

def load_seen_posts() -> set:
    """Load previously seen post IDs"""
    if TRACKER_FILE.exists():
        try:
            with open(TRACKER_FILE, 'r') as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_seen_posts(post_ids: set):
    """Save seen post IDs"""
    try:
        with open(TRACKER_FILE, 'w') as f:
            json.dump(list(post_ids), f)
    except Exception as e:
        print(f"Error saving tracker: {e}")

def get_new_posts(current_posts: list) -> list:
    """Filter posts to only return new ones"""
    seen = load_seen_posts()
    new_posts = []
    
    for post in current_posts:
        post_id = post.get("id") or post.get("title", "")
        if post_id not in seen:
            new_posts.append(post)
            seen.add(post_id)
    
    save_seen_posts(seen)
    return new_posts
