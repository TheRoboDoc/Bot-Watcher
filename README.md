# Discord Bot Watcher

A headless Python daemon to monitor the online status of your Discord bots and alert you via DM if any go offline.

## Features
- Periodically checks presence status of configured bot IDs
- Logs results to both file and terminal
- Sends you a Discord DM if any bot is offline or unreachable
- Fully configurable via `config.yaml`
- Designed to run persistently via `systemd` or `tmux`

## Requirements
- Python 3.10+
- A monotorin bot (must be in the same server as bots being watched)
- `discord.py`, `PyYAML`

## Installation

1. Clone or copy this repository

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create and edit `config.yaml`

```yaml
# Discord user ID to receive alerts via DM
owner_id: 0

# Time between checks in seconds
interval: 300

# Watcher bot's token
watcher_token: "YOUR_WATCHER_BOT_TOKEN"

# Path to write logs
log_path: "~/bot_watcher.log"

# List of Discord bot user IDs to monitor
bots:
  - 000000000000000000
  - 111111111111111111
```

5. Run the watcher

```bash
python bot_watcher.py
```

## Running as a Service (Linux)

Create a systemd unit:
```ini
# /etc/systemd/system/bot-watcher.service

[Unit]
Description=Discord Bot Watcher Service
After=network.target

[Service]
User=youruser
WorkingDirectory=/path/to/discord-bot-watcher
ExecStart=/path/to/discord-bot-watcher/venv/bin/python bot_watcher.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable --now bot-watcher.service
```

## Notes
- All monitored bots must be in a **shared guild** with the watcher bot.
- Bots must expose presence (`presence intent` enabled in developer portal)

---

Glory to the Machine.