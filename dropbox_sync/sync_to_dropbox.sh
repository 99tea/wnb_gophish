#!/bin/bash

WATCH_DIR="/opt/mailgun_webhooks/csv"
DEST="dropbox:/csv_webhooks"
LOG_FILE="/var/log/rclone_sync.log"
RCLONE_CONFIG="/opt/mailgun_webhooks/.config/rclone/rclone.conf"

echo "Monitoring $WATCH_DIR for changes..."
inotifywait -m -e close_write,moved_to,create "$WATCH_DIR" --format "%w%f" | while read file
do
    echo "$(date): Change detected: $file" | tee -a "$LOG_FILE"

    # Avoid running sync too frequently
    echo "Waiting 30 seconds before syncing..." | tee -a "$LOG_FILE"
    sleep 30

    echo "Syncing files..." | tee -a "$LOG_FILE"
    rclone sync "$WATCH_DIR" "$DEST" --config "$RCLONE_CONFIG" --progress --log-file="$LOG_FILE"
done

