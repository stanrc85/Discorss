# RSS to Discord Webhook Notifier

This Python script monitors Git Release RSS feeds and sends notifications to a Discord webhook when new updates are published. It uses a configuration file for easy management of RSS URLs and the Discord webhook URL.

## Features

* **RSS Feed Monitoring:** Checks multiple RSS feeds at a specified interval.
* **Discord Webhook Integration:** Sends notifications to a Discord channel via a webhook.
* **Post Caching:** Prevents duplicate notifications by caching processed post IDs.
* **Configurable RSS URLs and Webhook:** Uses a `config.ini` file for easy configuration.
* **Post Age Filtering:** Only sends notifications for posts published within a specified time frame.
* **Robust Date Handling:** Handles various date/time formats and timezones.

## Prerequisites

* Python 3.6 or higher
* `feedparser` library
* `requests` library
* `configparser` library
* `python-dateutil` library

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://gitea.stanley.cloud/Ryan/discorss.git
    cd discorss
    ```

2.  **Install the required Python libraries:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Create `config.ini`:**

    Create a `config.ini` file in the same directory as the script. Example:

    ```ini
    [RSS]
    urls =
        https://example.com/rss1
        https://example.com/rss2

    [Discord]
    webhook_url = YOUR_DISCORD_WEBHOOK_URL
    ```

    * Replace `YOUR_DISCORD_WEBHOOK_URL` with your actual Discord webhook URL.
    * Add your RSS feed URLs under the `[RSS]` section, one per line.

2.  **Configure `CHECK_INTERVAL` and `MAX_POST_AGE_DAYS`:**

    You can modify these variables in the script to adjust the checking interval and the maximum post age for notifications.

    ```python
    CHECK_INTERVAL = 300  # Check every 5 minutes (300 seconds)
    MAX_POST_AGE_DAYS = 1 # Only alert on posts younger than 1 day.
    ```

## Usage

1.  **Run the script:**

    ```bash
    python discorss.py
    ```

2.  The script will run continuously, checking the RSS feeds at the specified interval and sending notifications to your Discord channel.

## Running as a Service

To run the script as a background service:

* **Linux/macOS:** Use `nohup` or `screen` or `systemd` or `pm2`.
* **Windows:** Use Task Scheduler.

Example using `nohup` (Linux/macOS):

```bash
nohup python discorss.py &