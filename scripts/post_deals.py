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
    # Remove source indicators like [Steam], (GOG), etc.
    title = re.sub(r'\[(.*?)\]|\((.*?)\)', '', title)
    # Remove extra whitespace
    title = ' '.join(title.split())
    return title

for feed_url in feeds:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        title = clean_title(entry.title)
        link = entry.link
        
        if link in posted_links:
            continue
            
        message = f"🎮 **FREE GAME**: {title}\n{link}"
        posted_links.add(link)
        
        response = requests.post(
            WEBHOOK_URL,
            json={"content": message}
        )
        
        if response.status_code == 204:
            print(f"Posted: {title}")
        else:
            print(f"Failed to post: {title}, Status: {response.status_code}")
