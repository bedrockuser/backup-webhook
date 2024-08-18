import os, time, requests, zipfile, shutil, schedule, json
from pathlib import Path
from datetime import datetime

# Environment variables for configuration
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
MONITOR_FOLDER = os.getenv('MONITOR_FOLDER')
SEND_HOUR = os.getenv('SEND_HOUR', '01:00')  # default 1 AM
WEBHOOK_USERNAME = os.getenv('WEBHOOK_USERNAME', 'Backup Bot')
WEBHOOK_AVATAR_URL = os.getenv('WEBHOOK_AVATAR_URL', '')
TEMP_ZIP_PATH = '/tmp/backup.zip'

def compress_folder(folder_path, output_path):
    """Compress the folder into a ZIP file."""
    folder = Path(folder_path)
    if not folder.exists():
        print(f"Folder {folder_path} does not exist.")
        return False

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder)
                zipf.write(file_path, arcname=arcname)
    return True

def send_zip_to_webhook():
    """Send the compressed folder to the Discord webhook."""
    # Compress the folder
    if not compress_folder(MONITOR_FOLDER, TEMP_ZIP_PATH):
        print("Failed to compress the folder. Skipping send.")
        return

    # Send the compressed file to the webhook
    data = {
        "content": "Backup of folder at {}".format(datetime.now().strftime('%Y-%m-%d %H:%M')),
        "username": WEBHOOK_USERNAME,
        "avatar_url": WEBHOOK_AVATAR_URL
    }

    with open(TEMP_ZIP_PATH, 'rb') as file_data:
        files = {
            'payload_json': (None, json.dumps(data)),
            'file': ('backup.zip', file_data, 'application/zip'),
        }
        response = requests.post(WEBHOOK_URL, files=files)

    # Cleanup the temp file
    if os.path.exists(TEMP_ZIP_PATH):
        os.remove(TEMP_ZIP_PATH)

    if response.status_code == 204:
        print("Success: Backup sent to webhook.")
    else:
        print(f"Error: Failed to send backup. Status code: {response.status_code}")

def schedule_backup():
    """Schedule the backup based on the specified hour."""
    print(f"Scheduling backup every day at {SEND_HOUR}.")
    schedule.every().day.at(SEND_HOUR).do(send_zip_to_webhook)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    send_zip_to_webhook()  # Optionally run the first one immediately
    schedule_backup()
