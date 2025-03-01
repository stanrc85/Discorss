import feedparser
import requests
import time
import hashlib
import json
import configparser
import html2text  # Import the html2text library
from datetime import date, datetime, timedelta
from dateutil import parser, tz
import datetime

# Configuration
CONFIG_FILE = "config.ini"
CACHE_FILE = "rss_cache.json"
CHECK_INTERVAL = 60  # Check for updates every 5 minutes (300 seconds)
MAX_POST_AGE_DAYS = 1 # Only alert on posts younger than 1 day.

def load_config(filename):
    """Loads configuration from a file."""
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def load_rss_urls(config):
    """Loads RSS URLs from the configuration."""
    try:
        return [url.strip() for url in config["RSS"]["urls"].splitlines() if url.strip()]
    except KeyError:
        print("Error: RSS URLs not found in config file.")
        return []

def load_webhook_url(config):
    """Loads webhook URL from the configuration."""
    try:
        return config["Discord"]["webhook_url"]
    except KeyError:
        print("Error: Webhook URL not found in config file.")
        return None

def load_cache(filename):
    """Loads cached post IDs from a JSON file."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_cache(cache, filename):
    """Saves cached post IDs to a JSON file."""
    with open(filename, "w") as f:
        json.dump(cache, f, indent=4)

def check_rss_feed(url, cache):
    """Checks an RSS feed for new posts."""
    try:
        feed = feedparser.parse(url)
        if not feed.entries:
            print(f"No entries found in {url}")
            return

        new_posts = []
        now = datetime.datetime.now(tz.UTC) #make now offset aware and utc.
        max_age = datetime.timedelta(days=MAX_POST_AGE_DAYS)

        for entry in feed.entries:
            post_id = entry.get("id") or entry.get("link")  # Use ID if available, otherwise link
            published_time_tuple = entry.get("updated")
            # Parse the published time string into a datetime object
            published_time = parser.parse(published_time_tuple)
            post_age = now - published_time
            if post_id and post_id not in cache.get(url, []) and post_age <= max_age:
                new_posts.append(entry)
                if url not in cache:
                    cache[url]=[]
                cache[url].append(post_id)

        return new_posts

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return []

def send_discord_message(webhook_url, entry, feed_title):
    """Sends a message to a Discord webhook."""
    h = html2text.HTML2Text() #initialize the converter
    h.ignore_links = False #keep links.
    h.ignore_images = True #ignore images.
    try:
        title = entry.get("title", "Untitled")
        link = entry.get("link", "")
        description_html = getattr(entry, 'description', "No description available.")
        description_markdown = h.handle(description_html) #convert to markdown
        timestamp = entry.get("updated")

        embed = {
            "title": f"[{feed_title}] {title}",  # Use feed_title in the embed title
            "url": link,
            "description": description_markdown,
            "timestamp": timestamp
        }
        payload = {
            "embeds": [embed]
        }
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print(f"Sent message for: {title}")

    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Discord: {e}")
    except KeyError as e:
        print(f"Error parsing entry: {e}")

def main():
    """Main function to check RSS feeds and send messages."""
    config = load_config(CONFIG_FILE)
    rss_urls = load_rss_urls(config)
    webhook_url = load_webhook_url(config)
    cache = load_cache(CACHE_FILE)

    if not webhook_url:
        return

    while True:
        for url in rss_urls:
            # Get the feed title
            feed = feedparser.parse(url)
            feed_title = feed.feed.title  # Access the feed title
            new_posts = check_rss_feed(url, cache)
            if new_posts:
                for post in new_posts:
                    send_discord_message(webhook_url, post, feed_title)
        save_cache(cache, CACHE_FILE)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()