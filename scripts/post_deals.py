import feedparser
import requests
import os
import re

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

feeds = [
    "https://github.com/eikowagenknecht/lootscraper/feed",
    "https://www.reddit.com/r/GameDealsFree/.rss"
]

posted_links = set()

def clean_title(title):
    # Remove source indicators and platform tags
    title = re.sub(r'\[(.*?)\]|\((.*?)\)', '', title)
    # Remove "Free" mentions as we'll add our own
    title = re.sub(r'\bfree\b', '', title, flags=re.IGNORECASE)
    # Clean up extra whitespace
    title = ' '.join(title.split())
    return title

def create_embed(title, link):
    return {
        "embeds": [{
            "title": "🎮 New Free Game Available!",
            "description": f"**{title}**\n\n[**Claim Now →**]({link})",
            "color": 5793266,  # Green color
            "footer": {
                "text": "Limited time offer • Claim while available"
            }
        }]
    }

for feed_url in feeds:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        title = clean_title(entry.title)
        link = entry.link
        
        if link in posted_links:
            continue
            
        response = requests.post(
            WEBHOOK_URL,
            json=create_embed(title, link)
        )
        
        if response.status_code == 204:
            print(f"Posted: {title}")
        else:
            print(f"Failed to post: {title}, Status: {response.status_code}")
        
        posted_links.add(link)
