# python-disk-manager
This is a disk manager that I built for my server that I have a few internal servers running out of that generate logs. Due to working shift-work I often find it hard to keep track of the space, however I didn't want to implement retention rules on the server as I like to manually decide whether backups and logs can be removed, or moved to my personal hard-drive from the server. 

## Overview
Monitors disk usage and sends periodic Discord notifications into a specific channel, and tags the user. One of the big users of disk-space on my server has been a long-going minecraft world that creates backups hourly via node.js. This is and the associated nodejs logs can create large issues with disk space, due to this reasoning I have my application running every three hours to notify me.

## Features
- Reports free, used, and total disk space
- Sends alerts to a Discord channel
- Runs on a schedule

## Requirements
- Python 3.10+
- Linux
- `discord.py`
- `dotenv`

## Setup
1. Install dependencies:
    ```bash
    pip install discord.py python-dotenv
    ```
2. Create a `.env` file in `src/` with:
    - `DISCORD_TOKEN`
    - `CHANNEL_ID`
    - `USER_ID`

## Usage
Run the scheduler:
```bash
python -m src.main
```

Run a single check:
```bash
python -m src.space
```

## Interval
Adjust the interval in `src/main.py` if you want a different schedule.