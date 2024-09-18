import feedparser
import time
from datetime import datetime
import pytz  # Install pytz if you haven't already: pip install pytz
from dateutil import parser

# URL of the RSS feed to monitor
RSS_FEED_URLS = [
                'https://feeds.bloomberg.com/markets/news.rss',
                'https://feeds.bloomberg.com/economics/news.rss',
                'https://feeds.bloomberg.com/industries/news.rss',
                "https://finance.yahoo.com/news/rssindex",
                "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
                "https://www.ft.com/news-feed?format=rss.&page=1",
                "https://seekingalpha.com/market_currents.xml"
                ] 


# Function to fetch and parse the RSS feed
def fetch_feed(url):
    return feedparser.parse(url)

# Function to check for new items
def check_for_new_items(feed, known_entries):
    new_items = []
    for entry in feed.entries:
        if entry.id not in known_entries:
            new_items.append(entry)
            known_entries.add(entry.id)
    return new_items

def convert_published_date(published):
    try:
        # Parse the date (it can handle ISO 8601 and other formats)
        if isinstance(published, str):
            parsed_date = parser.parse(published)
        else:
            # If it's a struct_time object (from feedparser), convert it
            parsed_date = datetime(*published[:6])

        # Convert to UTC timezone if necessary
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=pytz.utc)
        
        # Convert to EST
        est_zone = pytz.timezone('America/New_York')
        est_date = parsed_date.astimezone(est_zone)

        # Format the datetime object into 'YYYY-MM-DD HH:MM:SS'
        formatted_date = est_date.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date

    except Exception as e:
        # Handle exceptions and return a default message or None
        print(f"Error converting date: {e}")
        return None

# Main function to monitor the RSS feeds
def monitor_feeds():
    known_entries = set()
    while True:
        for url in RSS_FEED_URLS:
            feed = fetch_feed(url)
            new_items = check_for_new_items(feed, known_entries)
            for item in new_items:
                published_date = convert_published_date(item.published_parsed)
                print(f"****************************** NEW ********************************")
                print("\n")
                print(f"{item.title}")
                print("\n")
                print(f"LINK: {item.link}")
                print("\n")
                print(f"SUMMARY: {getattr(item, 'summary', 'No summary available')}")
                print("\n")
                print(f"PUBLISHED: {published_date}")
                print("----------------------------------------------------------------------")
                print("\n")
        time.sleep(20)  # Check every 60 seconds
        print('Checking for new articles...')

if __name__ == "__main__":
    monitor_feeds()