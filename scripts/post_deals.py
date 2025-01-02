import feedparser
import requests
import os
import re
from urllib.parse import quote

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

feeds = [
    "https://github.com/eikowagenknecht/lootscraper/feed",
    "https://www.reddit.com/r/GameDealsFree/.rss"
]

posted_links = set()

def clean_title(title):
    title = re.sub(r'\[(.*?)\]|\((.*?)\)', '', title)
    title = re.sub(r'\bfree\b', '', title, flags=re.IGNORECASE)
    return ' '.join(title.split())

def get_steam_image(game_name):
    try:
        search_url = f"https://store.steampowered.com/api/storesearch/?term={quote(game_name)}&l=en"
        response = requests.get(search_url)
        data = response.json()
        if data.get('total') > 0:
            return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{data['items'][0]['id']}/header.jpg"
    except:
        pass
    return None

def create_embed(title, link):
    embed = {
        "embeds": [{
            "title": title,
            "url": link,
            "color": 3447003,
            "author": {
                "name": "Free Game Alert",
                "icon_url": "https://cdn.discordapp.com/emojis/1039663378205925466.webp"
            },
            "description": f"[Click to Claim →]({link})",
            "footer": {
                "text": "Limited Time Offer"
            }
        }],
        "components": [{
            "type": 1,
            "components": [{
                "type": 2,
                "style": 5,
                "label": "Claim Now",
                "url": link
            }]
        }]
    }
    
    image_url = get_steam_image(title)
    if image_url:
        embed["embeds"][0]["image"] = {"url": image_url}
    
    return embed

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
