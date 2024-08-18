# Backup-Webhook Docker Image

This Docker container monitors a specified folder, compresses it, and sends it to a Discord webhook at a specific time every day (configurable via environment variables).

## Features

- Sends a compressed ZIP file of the monitored folder to a Discord webhook.
- Configurable daily send time via environment variables.
- Customizable webhook username and avatar.

## Configuration

Configuration is done via environment variables:

- `WEBHOOK_URL`: The Discord webhook URL where the folder's backup will be sent.
- `MONITOR_FOLDER`: The folder to be monitored and sent as a ZIP.
- `SEND_HOUR`: The time of day (in 24-hour format) when the backup should be sent (e.g., `01:00` for 1 AM).
- `WEBHOOK_USERNAME`: The name that will appear on the webhook.
- `WEBHOOK_AVATAR_URL`: The avatar that will appear on the webhook.

## Example Docker Compose Setup

You can configure the service using `docker-compose.yml`. Below is an example setup:

```yaml
version: '3.8'

services:
  backup-webhooks:
    image: ghcr.io/bedrockuser/backup-webhook:latest
    build: .
    environment:
      - WEBHOOK_URL=YOUR_DISCORD_WEBHOOK_URL
      - MONITOR_FOLDER=/app/folder
      - SEND_HOUR=01:00  # Time to send the backup (24-hour format)
      - WEBHOOK_USERNAME=Backup Bot
      - WEBHOOK_AVATAR_URL=https://example.com/avatar.png
    volumes:
      - /path/to/local/folder:/app/folder
    restart: unless-stopped
