# RSS to Discord Webhook

This Python script monitors RSS feeds and posts new entries to a Discord webhook. It uses a configuration file to manage multiple feeds and a single shared webhook.

## Features

* **Multiple RSS Feed Support:** Monitors multiple RSS feeds defined in a configuration file.
* **Discord Webhook Integration:** Posts new entries to a specified Discord webhook.
* **Persistent Entry Tracking:** Prevents duplicate posts by tracking processed entries in a JSON file.
* **Markdown Conversion:** Converts HTML descriptions from RSS feeds to Markdown for cleaner Discord messages.
* **Configurable Interval:** Sets the frequency of RSS feed checks through a configuration setting.
* **Error Handling:** Robust error handling for RSS feed parsing, network issues, and Discord webhook errors.
* **Configuration File:** Uses a configuration file for easy management of RSS feeds and settings.

## Prerequisites

* Python 3.6 or higher
* `feedparser` library (`pip install feedparser`)
* `requests` library (`pip install requests`)
* `html2text` library (`pip install html2text`)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://gitea.stanley.cloud/Ryan/discorss.git
    cd discorss
    ```

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Create a `config.ini` file:**
    * Create a `config.ini` file in the same directory as the Python script.
    * Add your RSS feed URLs and Discord webhook URL to the `config.ini` file.

    ```ini
    [Feeds]
    Feed1 = [https://example.com/rss](https://example.com/rss)
    Feed2 = [https://anotherexample.com/feed](https://anotherexample.com/feed)
    Feed3 = [https://someotherfeed.com/rss](https://someotherfeed.com/rss)

    [General]
    sleep_interval = 120  ; Check every 2 minutes.
    processed_entries_file = my_processed_entries.json ; custom processed entries file name.
    webhook_url = [https://discord.com/api/webhooks/your/shared/webhook](https://discord.com/api/webhooks/your/shared/webhook)
    ```

    * Replace the placeholder URLs with your actual RSS feed and Discord webhook URLs.
    * Adjust the `sleep_interval` to your desired check frequency (in seconds).
    * `processed_entries_file` allows you to customize the file name of the JSON file used to track processed entries.

2.  **Get your Discord Webhook URL:**
    * In your Discord server, go to Server Settings > Integrations > Webhooks.
    * Create a new webhook and copy the webhook URL.

## Usage

1.  **Run the script:**
    ```bash
    python discorss.py
    ```

2.  The script will periodically check the RSS feeds and post new entries to your Discord channel.

## Troubleshooting

* **400 Bad Request:**
    * Verify that your Discord webhook URL is correct.
    * Check the `config.ini` file for any typos.
    * Check the response code and response content that are printed to the console for more information.
    * Simplify the embed payload to isolate the problem.
* **RSS Parsing Errors:**
    * Ensure that the RSS feed URLs are valid.
    * Check the RSS feed in a browser to verify its content.
* **Permission Errors:**
    * Ensure the script has write permissions to create and modify the `processed_entries.json` file.
* **Config file errors:**
    * Ensure the config file is in the same directory as the script.
    * Ensure all needed sections and variables are present.

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues.

## License

This project is licensed under the MIT License.