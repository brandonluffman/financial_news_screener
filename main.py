import feedparser
import asyncio
import websockets
from datetime import datetime
import pytz

import feedparser
import asyncio
import websockets

# List of RSS Feed URLs
rss_urls = [
    "https://feeds.bloomberg.com/markets/news.rss",
    "https://finance.yahoo.com/news/rssindex",
    "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "https://www.ft.com/news-feed?format=rss.&page=1",
    "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines",
    "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best",
    "https://www.investing.com/rss/news_25.rss",
    "https://seekingalpha.com/market_currents.xml",
    "https://markets.businessinsider.com/rss/news",
]

# Store the latest titles for each feed
latest_titles = {url: None for url in rss_urls}

# WebSocket clients list
connected_clients = set()

async def fetch_rss_feed():
    global latest_titles
    
    while True:
        for rss_url in rss_urls:
            feed = feedparser.parse(rss_url)
            
            if len(feed.entries) > 0:
                for entry in feed.entries:
                    title = entry.get('title', 'No Title Available')
                    link = entry.get('link', 'No Link Available')

                    if title != latest_titles[rss_url]:
                        latest_titles[rss_url] = title
                        new_article = {
                            "title": title,
                            "link": link,
                            "feed": rss_url
                        }
                        print(f"New article from {rss_url}: {title}")
                        print(f"Link: {link}")

                        # Notify all connected clients
                        await notify_clients(new_article)
        
        # Check the RSS feeds every 10 seconds
        await asyncio.sleep(10)

async def notify_clients(article):
    if connected_clients:
        message = (
            f"New article from {article['feed']}:\n"
            f"Title: {article['title']}\n"
            f"Link: {article['link']}"
        )
        await asyncio.wait([client.send(message) for client in connected_clients])

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        connected_clients.remove(websocket)

async def main():
    ws_server = await websockets.serve(handle_client, "localhost", 6789)
    print("WebSocket server started on ws://localhost:6789")

    await fetch_rss_feed()

asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()
