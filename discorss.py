import feedparser
import requests
import time
import hashlib
import json
import configparser
import html2text  # Import the html2text library

def load_config(config_file="config.ini"):
    """Loads configuration from a config file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def check_rss_feed(rss_url, webhook_url, processed_entries_file="processed_entries.json"):
    """
    Checks an RSS feed for new entries and posts them to a Discord webhook.

    Args:
        rss_url: The URL of the RSS feed.
        webhook_url: The Discord webhook URL.
        processed_entries_file: A JSON file to store processed entry hashes.
    """

    try:
        with open(processed_entries_file, "r") as f:
            processed_entries = json.load(f)
    except FileNotFoundError:
        processed_entries = {}
    except json.JSONDecodeError:
        processed_entries = {} #Handle potentially corrupted file
        print(f"Warning: {processed_entries_file} was corrupted. Starting with an empty processed entries list.")

    feed = feedparser.parse(rss_url)

    if feed.bozo == 1: #Handle parsing errors.
        print(f"Error parsing RSS feed: {feed.bozo_exception}")
        return

    if not hasattr(feed, 'entries'):
        print(f"Error: No entries found in the RSS feed: {rss_url}")
        return

    new_entries = []

    for entry in feed.entries:
        entry_hash = hashlib.sha256(entry.link.encode()).hexdigest() #Use link as unique ID.

        if rss_url not in processed_entries:
            processed_entries[rss_url] = []

        if entry_hash not in processed_entries[rss_url]:
            new_entries.append(entry)
            processed_entries[rss_url].append(entry_hash)

    if new_entries:
        h = html2text.HTML2Text() #initialize the converter
        h.ignore_links = False #keep links.
        h.ignore_images = True #ignore images.

        for entry in new_entries:
            title = entry.title
            link = entry.link
            description_html = getattr(entry, 'description', "No description available.")
            description_markdown = h.handle(description_html) #convert to markdown
            #published = getattr(entry, 'published', "Unknown publish date.") #Handle missing dates.
            embed = {
                "title": title,
                "url": link,
                "description": description_markdown,
                #"timestamp": published, #Discord can parse most ISO 8601 dates.
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

        with open(processed_entries_file, "w") as f:
            json.dump(processed_entries, f, indent=4) #Save updated processed entries.

    else:
        print("No new entries.")

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
        processed_entries_file = general.get("processed_entries_file", "processed_entries.json")
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

                check_rss_feed(rss_url, webhook_url, processed_entries_file)

            except Exception as e:
                print(f"An unexpected error occurred for {feed_name}: {e}")

        time.sleep(sleep_interval)