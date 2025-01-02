import feedparser
import requests
import os

# Get webhook URL from environment
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# RSS Feeds
feeds = [
    "https://github.com/eikowagenknecht/lootscraper/feed",
    "https://www.reddit.com/r/GameDealsFree/.rss"
]

# Track posted links
posted_links = set()

for feed_url in feeds:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        
        # Skip duplicates
        if link in posted_links:
            continue
            
        # Format message
        message = f"🎮 **{title}**\n{link}"
        posted_links.add(link)
        
        # Post to Discord
        response = requests.post(
            WEBHOOK_URL,
            json={"content": message}
        )
        
        if response.status_code == 204:
            print(f"Posted: {title}")
        else:
            print(f"Failed to post: {title}, Status: {response.status_code}")
