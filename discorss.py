import feedparser
import requests
import time
import hashlib
import json
import configparser
import html2text  # Import the html2text library
from datetime import date
from datetime import datetime

def load_config(config_file="config.ini"):
    """Loads configuration from a config file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def check_rss_feed(rss_url, webhook_url, feed_title):
    """
    Checks an RSS feed for new entries and posts them to a Discord webhook.
    """
    feed = feedparser.parse(rss_url)

    if feed.bozo == 1: #Handle parsing errors.
        print(f"Error parsing RSS feed: {feed.bozo_exception}")
        return

    if not hasattr(feed, 'entries'):
        print(f"Error: No entries found in the RSS feed: {rss_url}")
        return

    h = html2text.HTML2Text() #initialize the converter
    h.ignore_links = False #keep links.
    h.ignore_images = True #ignore images.

    current_date = date.today()
    print(current_date)

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        description_html = getattr(entry, 'description', "No description available.")
        description_markdown = h.handle(description_html) #convert to markdown
        published = getattr(entry, 'updated', "Unknown publish date.") #Handle missing dates.
        try:
            date_object = datetime.strptime(published, '%Y-%m-%d').date()
        except ValueError as ve1:
            print(ve1)
        print(date_object)
        if published < current_date:
            print(f"Old news")
        else:
            embed = {
                "title": f"[{feed_title}] {title}",  # Use feed_title in the embed title
                "url": link,
                "description": description_markdown,
                "timestamp": published, #Discord can parse most ISO 8601 dates.
            }

            payload = {
                "embeds": [embed]
            }

            try:
                response = requests.post(webhook_url, json=payload)
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                print(f"Posted: {title}")
            except requests.exceptions.RequestException as e:
                print(f"Error posting to Discord: {e}")

if __name__ == "__main__":
    config = load_config()

    try:
        feeds = config["Feeds"]
    except KeyError:
        print("Error: 'Feeds' section not found in config file.")
        exit(1)

    try:
        general = config["General"]
        sleep_interval = int(general.get("sleep_interval", 300))
        webhook_url = general["webhook_url"] #Get the single webhook from the general section.
    except KeyError as e:
        print(f"Error: Missing key in 'General' section: {e}")
        exit(1)

    while True:
        for feed_name, rss_url in feeds.items():
            try:
                rss_url = rss_url.strip() #remove extra spaces.
                if not rss_url:
                  print(f"Warning: Missing RSS URL for {feed_name}. Skipping.")
                  continue
                
                # Get the feed title
                feed = feedparser.parse(rss_url)
                feed_title = feed.feed.title  # Access the feed title
                check_rss_feed(rss_url, webhook_url, feed_title)

            except Exception as e:
                print(f"An unexpected error occurred for {feed_name}: {e}")

        time.sleep(sleep_interval)